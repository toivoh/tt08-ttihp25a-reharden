/*
 * SPDX-FileCopyrightText: 2024 Anton Maurovic <anton@maurovic.com>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * SPDX-License-Identifier: Apache-2.0
 */

#include <stdio.h>
// #include <err.h>
#include <iostream>
#include <string>
#include <vector>
#include <filesystem> // For std::filesystem::absolute() (which is only used if we have C++17)
#include "testbench.h"
using namespace std;

#include "Vcontroller.h" // Generated by Verilator

#define DESIGN      controller
#define VDESIGN     Vcontroller
#define MAIN_TB     Vcontroller_TB
#define BASE_TB     TESTBENCH<VDESIGN>

#define HILITE      0b0001'1111

//#define DESIGN_DIRECT_VECTOR_ACCESS   // Defined=new_playerX etc are exposed; else=SPI only.
//#define DEBUG_BUTTON_INPUTS
//#define USE_SPEAKER

// #define USE_POWER_PINS //NOTE: This is automatically set in the Makefile, now.
//#define INSPECT_INTERNAL //NOTE: This is automatically set in the Makefile, now.
#ifdef INSPECT_INTERNAL
  #include "Vcontroller_controller.h"       // Needed for accessing "verilator public" stuff in `controller`
#endif

#define FONT_FILE "font-cousine/Cousine-Regular.ttf"

#define CLOCK_HZ    25'000'000

#define S1(s1) #s1
#define S2(s2) S1(s2)

#include <SDL2/SDL.h>
// #include <SDL2/SDL_image.h> // This will be used for loading "ROMs" that interface with the design: Map & Texture data.
#include <SDL2/SDL_ttf.h>

// It would be nice if these could be retrieved directly from the Verilog (vga_sync.v).
// I think there's a way to do it with a "DPI" or some other Verilator method.
#define HDA 640    // Horizontal display area.
#define HFP 16     // Front porch (defined in this case to mean "coming after HDA, and before HSP").
#define HSP 96     // HSYNC pulse.
#define HBP 48     // Back porch (defined in this case to mean "coming after HSP").
#define VDA 480    // Vertical display area.
#define VFP 10     // Front porch.
#define VSP 2      // VSYNC pulse.
#define VBP 33     // Back porch.

#define HFULL (HDA+HFP+HSP+HBP)
#define VFULL (VDA+VFP+VSP+VBP)

// Extra space to show on the right and bottom of the virtual VGA screen,
// used for identifying extreme limits of things (and possible overflow):
#define EXTRA_RHS         50
#define EXTRA_BOT         50
#define H_OFFSET          HSP+HBP   // Left-hand margin during HSYNC pulse and HBP that comes before HDA.
#define V_OFFSET          VSP+VBP

#define REFRESH_PIXEL     1
#define REFRESH_SLOW      8
#define REFRESH_FASTPIXEL 100
#define REFRESH_LINE      HFULL
#define REFRESH_10LINES   HFULL*10
#define REFRESH_80LINES   HFULL*80
#define REFRESH_FRAME     HFULL*VFULL

// SDL window size in pixels. This is what our design's timing should drive in VGA:
#define WINDOW_WIDTH  (HFULL+EXTRA_RHS)
#define WINDOW_HEIGHT (VFULL+EXTRA_BOT)
#define FRAMEBUFFER_SIZE WINDOW_WIDTH*WINDOW_HEIGHT*4

// The MAIN_TB class that includes specifics about running our design in simulation:
#include "main_tb.h"


//SMELL: This doesn't do anything besides keeping certain linkers happy.
// See: https://veripool.org/guide/latest/faq.html#why-do-i-get-undefined-reference-to-sc-time-stamp
double sc_time_stamp() { return 0; }

#ifdef WINDOWS
//SMELL: For some reason, when building this under Windows, it stops building as a console command
// and instead builds as a Windows app requiring WinMain. Possibly something to do with Verilator
// or SDL2 under windows. I'm not sure yet. Anyway, this is a temporary workaround. The Makefile
// will include `-CFLAGS -DWINDOWS`, when required, in order to activate this code:
#include <windows.h>
int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
  // char* nothing = "nothing";
  // return main(1, &nothing);
  SetProcessDPIAware(); // Prevent window scaling, so we get a pixel-perfect SDL display.
  printf("DEBUG: WinMain command-line: '%s'\n", lpCmdLine);
  return main(__argc, __argv); // See: https://stackoverflow.com/a/40107581
  return 0;
}
#endif // WINDOWS


// Testbench for main design:
MAIN_TB       *TB;
bool          gQuit = false;
int           gRefreshLimit = REFRESH_FRAME;
int           gOriginalTime;
int           gPrevTime;
int           gPrevFrames;
unsigned long gPrevTickCount;
bool          gSyncLine = false;
bool          gSyncFrame = false;
bool          gHighlight = true;
bool          gGuides = false;
bool          gSwapMouseXY = false;
bool          gRotateView = false;
bool          gDisplayResync = false;
bool          gRenderDAC = true; // If false, just use TT08 'digital' outputs instead.
bool          gDisableR = false;
bool          gDisableG = false;
bool          gDisableB = false;
int           gMouseX, gMouseY;
#ifdef WINDOWS
bool          gMouseCapture = true;
#else
bool          gMouseCapture = false; // Not on by default in Linux, because of possible mouse relative motion weirdness.
#endif


//SMELL: @raybox leftovers:
enum {
  LOCK_F = 0,
  LOCK_B,
  LOCK_L,
  LOCK_R,
  LOCK_MAP,
  LOCK_DEBUG,
  LOCK__MAX
};
bool gLockInputs[LOCK__MAX] = {0};


// From: https://stackoverflow.com/a/38169008
// - x, y: upper left corner.
// - texture, rect: outputs.
void get_text_and_rect(
  SDL_Renderer *renderer,
  int x,
  int y,
  const char *text,
  TTF_Font *font,
  SDL_Texture **texture,
  SDL_Rect *rect
) {
  int text_width;
  int text_height;
  SDL_Surface *surface;
  SDL_Color textColor = {255, 255, 255, 0};

  surface = TTF_RenderText_Solid(font, text, textColor);
  *texture = SDL_CreateTextureFromSurface(renderer, surface);
  text_width = surface->w;
  text_height = surface->h;
  SDL_FreeSurface(surface);
  rect->x = x;
  rect->y = y;
  rect->w = text_width;
  rect->h = text_height;
}

void toggle_mouse_capture(bool force = false, bool force_to = false) {
  if (!force) {
    gMouseCapture = !gMouseCapture;
  } else {
    gMouseCapture = force_to;
  }
  if (gMouseCapture) {
    int r = SDL_SetRelativeMouseMode(SDL_TRUE);
    if (r) {
      printf("SDL_SetRelativeMouseMode(SDL_TRUE) failed (%d): %s\n", r, SDL_GetError());
    } else {
      printf("Mouse captured.\n");
      gMouseX = 0;
      gMouseY = 0;
    }
  } else {
    int r = SDL_SetRelativeMouseMode(SDL_FALSE);
    if (r) {
      printf("SDL_SetRelativeMouseMode(SDL_FALSE) failed (%d): %s\n", r, SDL_GetError());
    } else {
      printf("Mouse released.\n");
    }
  }
}


void tt_vga_fun_mode_base(int input, int final = -1) {
  // Assert reset:
  TB->m_core->rst_n = 0;
  // Apply mode to ui_in:
  TB->m_core->ui_in = input; //0_011_0000
  // Tick twice:
  TB->tick();
  TB->tick();
  // Now release reset:
  TB->m_core->rst_n = 1;
  // One more tick:
  TB->tick();
  if (final != -1) {
    // Now set final state of ui_in:
    TB->m_core->ui_in = final;
  }
  // Signal that we need a screen resync:
  gDisplayResync = true;
}


void tt_vga_fun_mode3() {
  tt_vga_fun_mode_base(0b00110000); // 0_011_xxxx = MODE_XORS
}

void tt_vga_fun_mode1(int primary) {
  tt_vga_fun_mode_base(0b00010000 | primary); //0_001_00pp = MODE_RAMP; pp = primary
}

void tt_vga_fun_mode0(int final) {
  tt_vga_fun_mode_base(0, final);
}

void tt_vga_fun_toggle_ui_in(int bits) {
  TB->m_core->ui_in ^= bits;
}

void tt_vga_fun_set_ui_in(int bits) {
  TB->m_core->ui_in = bits;
}


void process_sdl_events() {
  // Event used to receive window close, keyboard actions, etc:
  SDL_Event e;
  // Consume SDL events, if any, until the event queue is empty:
  while (SDL_PollEvent(&e) == 1) {
    if (SDL_QUIT == e.type) {
      // SDL quit event (e.g. close window)?
      gQuit = true;
    } else if (SDL_KEYDOWN == e.type) {
      int fn_key = 0;
      switch (e.key.keysym.sym) {
        case SDLK_F12:
          // Toggle mouse capture.
          toggle_mouse_capture();
          break;
        case SDLK_ESCAPE:
          gQuit = true;
          break;
        case SDLK_SPACE:
          TB->pause(!TB->paused);
          break;
        case SDLK_h:
          gHighlight = !gHighlight;
          printf("Highlighting turned %s\n", gHighlight ? "ON" : "off");
          break;
        case SDLK_t:
          gDisableR = !gDisableR;
          printf("Red channel rendering is now: %s\n", gDisableR ? "DISABLED":"Enabled");
          break;
        case SDLK_g:
          gDisableG = !gDisableG;
          printf("Green channel rendering is now: %s\n", gDisableG ? "DISABLED":"Enabled");
          break;
        case SDLK_b:
          gDisableB = !gDisableB;
          printf("Blue channel rendering is now: %s\n", gDisableB ? "DISABLED":"Enabled");
          break;
        case SDLK_1:
          gRefreshLimit = REFRESH_PIXEL;
          gSyncLine = false;
          gSyncFrame = false;
          printf("Refreshing every pixel\n");
          break;
        case SDLK_8:
          gRefreshLimit = REFRESH_SLOW;
          gSyncLine = false;
          gSyncFrame = false;
          printf("Refreshing every 8 pixels\n");
          break;
        case SDLK_9:
          gRefreshLimit = REFRESH_FASTPIXEL;
          gSyncLine = false;
          gSyncFrame = false;
          printf("Refreshing every 100 pixels\n");
          break;
        case SDLK_2:
          gRefreshLimit = REFRESH_LINE;
          gSyncLine = true;
          gSyncFrame = false;
          printf("Refreshing every line\n");
          break;
        case SDLK_3:
          gRefreshLimit = REFRESH_10LINES;
          gSyncLine = true;
          gSyncFrame = false;
          printf("Refreshing every 10 lines\n");
          break;
        case SDLK_4:
          gRefreshLimit = REFRESH_80LINES;
          gSyncLine = true;
          gSyncFrame = false;
          printf("Refreshing every 80 lines\n");
          break;
        case SDLK_5:
          gRefreshLimit = REFRESH_FRAME;
          gSyncLine = true;
          gSyncFrame = true;
          printf("Refreshing every frame\n");
          break;
        case SDLK_6:
          gRefreshLimit = REFRESH_FRAME*3;
          gSyncLine = true;
          gSyncFrame = true;
          printf("Refreshing every 3 frames\n");
          break;
        case SDLK_v:
          TB->log_vsync = !TB->log_vsync;
          printf("Logging VSYNC %s\n", TB->log_vsync ? "enabled" : "disabled");
          break;
        case SDLK_KP_PLUS:
          printf("gRefreshLimit increased to %d\n", gRefreshLimit+=1000);
          break;
        case SDLK_KP_MINUS:
          printf("gRefreshLimit decreated to %d\n", gRefreshLimit-=1000);
          break;
        case SDLK_x: // eXamine: Pause as soon as a frame is detected with any tone generation.
          TB->examine_mode = !TB->examine_mode;
          if (TB->examine_mode) {
            printf("Examine mode ON\n");
            TB->examine_condition_met = false;
          }
          else {
            printf("Examine mode off\n");
          }
          break;
        case SDLK_i:
          // Inspect: Print out current vector data as C++ code:
          printf("\nInspection not implemented.\n");
          // printf("\n// Vectors inspection data:\n");
          // uint32_t v;
          // v=TB->m_core->DESIGN->playerX; printf("TB->m_core->DESIGN->playerX = 0x%08X; // %lf\n", v, fixed2double(v));
          // // ...
          // printf("\n");
          if (KMOD_SHIFT & e.key.keysym.mod) {
            // Shift key held, so pause too.
            TB->pause(true);
          }
          break;
        case SDLK_s: // Step-examine, basically the same as hitting X then P while already paused.
          TB->examine_mode = true;
          TB->examine_condition_met = false;
          TB->pause(false); // Unpause.
          break;
        case SDLK_p:
          gRotateView = !gRotateView;
          printf("View is%s rotated\n", gRotateView ? "" : " NOT");
          break;
        case SDLK_o:
          gSwapMouseXY = !gSwapMouseXY;
          printf("Mouse axes are%s swapped\n", gSwapMouseXY ? "" : " NOT");
          break;
        // Turn off all input locks:
        case SDLK_END:    memset(&gLockInputs, 0, sizeof(gLockInputs)); break;

        default:

          if (KMOD_SHIFT & e.key.keysym.mod) {
            switch (e.key.keysym.sym) {
              // Specific modes we want to control:
              case SDLK_F1:
                tt_vga_fun_mode3(); // MODE_XORS
                break;
              case SDLK_F2:
                tt_vga_fun_mode1(0);  // MODE_RAMP: R pri, G sec, B fade.
                break;
              case SDLK_F3:
                tt_vga_fun_mode1(1);  // MODE_RAMP: R fade, G pri, B sec.
                break;
              case SDLK_F4:
                tt_vga_fun_mode1(2);  // MODE_RAMP: R sec, G fade, B pri.
                break;
              case SDLK_F5:
                tt_vga_fun_mode1(3);  // MODE_RAMP: All primary.
                break;
              case SDLK_F6:
                tt_vga_fun_mode0(127);  // MODE_PASS: With lum 127.
                break;
            }
          }
          else {
            int b = 0;
            switch (e.key.keysym.sym) {
              // Toggle a ui_in bit:
              case SDLK_F1: ++b;
              case SDLK_F2: ++b;
              case SDLK_F3: ++b;
              case SDLK_F4: ++b;
              case SDLK_F5: ++b;
              case SDLK_F6: ++b;
              case SDLK_F7: ++b;
              case SDLK_F8:
                tt_vga_fun_toggle_ui_in(1<<b);
                break;
              case SDLK_F9:
                // Set all:
                tt_vga_fun_set_ui_in(0b11111111);
                break;
              case SDLK_F10:
                // Clear all:
                tt_vga_fun_set_ui_in(0);
                break;
              case SDLK_F11:
                // Toggle DAC mode:
                gRenderDAC = !gRenderDAC;
                printf(gRenderDAC ? "Rendering uo_out digital outputs\n" : "Rendering DAC analog output simulation\n");
                break;
            }
          }

          // Not in Override Vectors mode; let the design handle motion.
          switch (e.key.keysym.sym) {
            case SDLK_BACKQUOTE: //NOTE: As a scancode, the backtick is SDL_SCANCODE_GRAVE.
              gLockInputs[LOCK_DEBUG] ^= 1; break;
#ifdef DESIGN_DIRECT_VECTOR_ACCESS
            // Toggle map input:
            case SDLK_INSERT: gLockInputs[LOCK_MAP] ^= 1; break;
            // Toggle direction inputs (and turn off any that are opposing):
            case SDLK_UP:     if (KMOD_SHIFT & e.key.keysym.mod) TB->m_core->moveF=1; else if( (gLockInputs[LOCK_F] ^= 1) ) gLockInputs[LOCK_B] = false; break;
            case SDLK_DOWN:   if (KMOD_SHIFT & e.key.keysym.mod) TB->m_core->moveB=1; else if( (gLockInputs[LOCK_B] ^= 1) ) gLockInputs[LOCK_F] = false; break;
            case SDLK_LEFT:   if (KMOD_SHIFT & e.key.keysym.mod) TB->m_core->moveL=1; else if( (gLockInputs[LOCK_L] ^= 1) ) gLockInputs[LOCK_R] = false; break;
            case SDLK_RIGHT:  if (KMOD_SHIFT & e.key.keysym.mod) TB->m_core->moveR=1; else if( (gLockInputs[LOCK_R] ^= 1) ) gLockInputs[LOCK_L] = false; break;
            // NOTE: If SHIFT is held, send momentary (1-frame) signal inputs instead of locks.
            //SMELL: This won't work if we're calling handle_control_inputs more often than once per frame...?
#endif//DESIGN_DIRECT_VECTOR_ACCESS
          }
          break;
      }
    }
  }
}


//NOTE: handle_control_inputs is called twice; once with `true` before process_sdl_events, then once after with `false`.
void handle_control_inputs(bool prepare, double t) {
  if (prepare) {
    // PREPARE mode: Clear all inputs, so process_sdl_events has a chance to preset MOMENTARY inputs:
    TB->m_core->rst_n     = 1;
  #ifdef DESIGN_DIRECT_VECTOR_ACCESS
      TB->m_core->show_map  = 0;
      TB->m_core->moveF     = 0;
      TB->m_core->moveL     = 0;
      TB->m_core->moveB     = 0;
      TB->m_core->moveR     = 0;
  #endif//DESIGN_DIRECT_VECTOR_ACCESS

#ifdef DEBUG_BUTTON_INPUTS
    TB->m_core->debugA    = 0;
    TB->m_core->debugB    = 0;
    TB->m_core->debugC    = 0;
    TB->m_core->debugD    = 0;
#endif // DEBUG_BUTTON_INPUTS
  }
  else {

    int mouseX, mouseY;
    if (gMouseCapture) {
      uint32_t buttons = SDL_GetRelativeMouseState(&mouseX, &mouseY);
      gMouseX += mouseX;
      gMouseY += mouseY;
    } else {
      mouseX = 0;
      mouseY = 0;
    }

    // ACTIVE mode: Read the momentary state of all keyboard keys, and add them via `|=` to whatever is already asserted:
    auto keystate = SDL_GetKeyboardState(NULL);

    // TB->m_core->ui_in = 0x30; //0b0_011_0000;

    TB->m_core->rst_n    &= !keystate[SDL_SCANCODE_R];
    // TB->m_core->i_debug   = gLockInputs[LOCK_DEBUG]; // | keystate[SDL_SCANCODE_GRAVE];
    // TB->m_core->i_inc_px  = keystate[SDL_SCANCODE_LEFTBRACKET];
    // TB->m_core->i_inc_py  = keystate[SDL_SCANCODE_RIGHTBRACKET];

    #ifdef DESIGN_DIRECT_VECTOR_ACCESS
      TB->m_core->moveF     |= keystate[SDL_SCANCODE_W   ] | gLockInputs[LOCK_F];
      TB->m_core->moveL     |= keystate[SDL_SCANCODE_A   ] | gLockInputs[LOCK_L];
      TB->m_core->moveB     |= keystate[SDL_SCANCODE_S   ] | gLockInputs[LOCK_B];
      TB->m_core->moveR     |= keystate[SDL_SCANCODE_D   ] | gLockInputs[LOCK_R];
    #endif//DESIGN_DIRECT_VECTOR_ACCESS

#ifdef DEBUG_BUTTON_INPUTS
    TB->m_core->debugA    |= keystate[SDL_SCANCODE_KP_4];
    TB->m_core->debugB    |= keystate[SDL_SCANCODE_KP_6];
    TB->m_core->debugC    |= keystate[SDL_SCANCODE_KP_2];
    TB->m_core->debugD    |= keystate[SDL_SCANCODE_KP_8];
#endif // DEBUG_BUTTON_INPUTS
  }
}



void check_performance() {
  uint32_t time_now = SDL_GetTicks();
  uint32_t time_delta = time_now-gPrevTime;

  if (time_delta >= 1000) {
    // 1S+ has elapsed, so print FPS:
    printf("Current FPS: %5.2f", float(TB->frame_counter-gPrevFrames)/float(time_delta)*1000.0f);
    // Estimate clock speed based on delta of m_tickcount:
    //SMELL: This code is really weird because for some bizarre reason I was getting mixed results
    // between Windows and Linux builds. It was as though sometimes on Windows it was treating a
    // LONG as a 32-bit integer, especially when doing *1000L
    long a = gPrevTickCount;
    long b = TB->m_tickcount;
    long c = (b-a);
    long d = time_delta;
    long hz = c / d;
    hz *= 1000L;
    // Now print long-term average:
    printf(" - Total average FPS: %5.2f", float(TB->frame_counter)/float(time_now-gOriginalTime)*1000.0f);
    // printf(" - a=%ld b=%ld c=%ld, d=%ld, hz=%ld", a, b, c, d, hz);
    printf(" - m_tickcount=");
    TB->print_big_num(TB->m_tickcount);
    printf(" (");
    TB->print_big_num(hz);
    printf(" Hz; %3ld%% of target)\n", (hz*100)/CLOCK_HZ);
    gPrevTime = SDL_GetTicks();
    gPrevFrames = TB->frame_counter;
    gPrevTickCount = TB->m_tickcount;
  }
}



void clear_freshness(uint8_t *fb) {
  // If we're not refreshing at least one full frame at a time,
  // then clear the "freshness" of pixels that haven't been updated.
  // We make this conditional in the hopes of getting extra speed
  // for higher refresh rates.
  // if (gRefreshLimit < REFRESH_FRAME) {
    // In this simulation, the 6 lower bits of each colour channel
    // are not driven by the design, and so we instead use them to
    // help visualise what region of the framebuffer has been updated
    // between SDL window refreshes (by the rendering loop forcing them on,
    // which appears as a slight brightening).
    // THIS loop clears all that between refreshes:
    for (int x = 0; x < HFULL; ++x) {
      for (int y = 0; y < VFULL; ++y) {
        fb[(x+y*WINDOW_WIDTH)*4 + 0] &= ~HILITE;
        fb[(x+y*WINDOW_WIDTH)*4 + 1] &= ~HILITE;
        fb[(x+y*WINDOW_WIDTH)*4 + 2] &= ~HILITE;
      }
    }
  // }
}

void overlay_display_area_frame(uint8_t *fb, int h_shift = 0, int v_shift = 0) {
  // if (!gGuides) return;
  // Vertical range: Horizontal lines (top and bottom):
  if (v_shift > 0) {
    for (int x = 0; x < WINDOW_WIDTH; ++x) {
      fb[(x+(v_shift-1)*WINDOW_WIDTH)*4 + 0] |= 0b0100'0000;
      fb[(x+(v_shift-1)*WINDOW_WIDTH)*4 + 1] |= 0b0100'0000;
      fb[(x+(v_shift-1)*WINDOW_WIDTH)*4 + 2] |= 0b0100'0000;
    }
  }
  if (v_shift+VDA < WINDOW_HEIGHT) {
    for (int x = 0; x < WINDOW_WIDTH; ++x) {
      fb[(x+(VDA+v_shift)*WINDOW_WIDTH)*4 + 0] |= 0b0100'0000;
      fb[(x+(VDA+v_shift)*WINDOW_WIDTH)*4 + 1] |= 0b0100'0000;
      fb[(x+(VDA+v_shift)*WINDOW_WIDTH)*4 + 2] |= 0b0100'0000;
    }
  }
  // Horizontal range: Vertical lines (left and right sides):
  if (h_shift > 0) {
    for (int y = 0; y < WINDOW_HEIGHT; ++y) {
      fb[(h_shift-1+y*WINDOW_WIDTH)*4 + 0] |= 0b0100'0000;
      fb[(h_shift-1+y*WINDOW_WIDTH)*4 + 1] |= 0b0100'0000;
      fb[(h_shift-1+y*WINDOW_WIDTH)*4 + 2] |= 0b0100'0000;
    }
  }
  if (h_shift+HDA < WINDOW_WIDTH) {
    for (int y = 0; y < WINDOW_HEIGHT; ++y) {
      fb[(HDA+h_shift+y*WINDOW_WIDTH)*4 + 0] |= 0b0100'0000;
      fb[(HDA+h_shift+y*WINDOW_WIDTH)*4 + 1] |= 0b0100'0000;
      fb[(HDA+h_shift+y*WINDOW_WIDTH)*4 + 2] |= 0b0100'0000;
    }
  }
  // Guides:
  if (gGuides) {
    // Mid-screen vertical line:
    for (int y = 0; y < WINDOW_HEIGHT; ++y) {
        fb[(HDA/2+h_shift+y*WINDOW_WIDTH)*4 + 0] |= 0b0110'0000;
        fb[(HDA/2+h_shift+y*WINDOW_WIDTH)*4 + 1] |= 0b0110'0000;
        fb[(HDA/2+h_shift+y*WINDOW_WIDTH)*4 + 2] |= 0b0110'0000;
    }
    // Mouse crosshairs:
    // X axis, vertical line:
    int mx = gMouseX + HDA/2;
    int my = gMouseY + VDA/2;
    if (mx >= 0 && mx < HDA) {
      for (int y = 0; y < WINDOW_HEIGHT; ++y) {
          fb[(mx+h_shift+y*WINDOW_WIDTH)*4 + 0] |= 0b0110'0000;
          fb[(mx+h_shift+y*WINDOW_WIDTH)*4 + 1] |= 0b0110'0000;
          fb[(mx+h_shift+y*WINDOW_WIDTH)*4 + 2] |= 0b0110'0000;
      }
    }
    if (my >= 0 && my < VDA) {
      for (int x = 0; x < WINDOW_WIDTH; ++x) {
          fb[(x+(my+v_shift)*WINDOW_WIDTH)*4 + 0] |= 0b0110'0000;
          fb[(x+(my+v_shift)*WINDOW_WIDTH)*4 + 1] |= 0b0110'0000;
          fb[(x+(my+v_shift)*WINDOW_WIDTH)*4 + 2] |= 0b0110'0000;
      }
    }
  }
}


void fade_overflow_region(uint8_t *fb) {
  for (int x = HFULL; x < WINDOW_WIDTH; ++x) {
    for (int y = 0 ; y < VFULL; ++y) {
      fb[(x+y*WINDOW_WIDTH)*4 + 0] *= 0.95;
      fb[(x+y*WINDOW_WIDTH)*4 + 1] *= 0.95;
      fb[(x+y*WINDOW_WIDTH)*4 + 2] *= 0.95;
    }
  }
  for (int x = 0; x < WINDOW_WIDTH; ++x) {
    for (int y = VFULL; y < WINDOW_HEIGHT; ++y) {
      fb[(x+y*WINDOW_WIDTH)*4 + 0] *= 0.95;
      fb[(x+y*WINDOW_WIDTH)*4 + 1] *= 0.95;
      fb[(x+y*WINDOW_WIDTH)*4 + 2] *= 0.95;
    }
  }
}


void overflow_test(uint8_t *fb) {
  for (int x = HFULL; x < WINDOW_WIDTH; ++x) {
    for (int y = 0 ; y < VFULL; ++y) {
      fb[(x+y*WINDOW_WIDTH)*4 + 0] = 50;
      fb[(x+y*WINDOW_WIDTH)*4 + 1] = 150;
      fb[(x+y*WINDOW_WIDTH)*4 + 2] = 255;
    }
  }
  for (int x = 0; x < WINDOW_WIDTH; ++x) {
    for (int y = VFULL; y < WINDOW_HEIGHT; ++y) {
      fb[(x+y*WINDOW_WIDTH)*4 + 0] = 50;
      fb[(x+y*WINDOW_WIDTH)*4 + 1] = 150;
      fb[(x+y*WINDOW_WIDTH)*4 + 2] = 255;
    }
  }
}



void render_text(SDL_Renderer* renderer, TTF_Font* font, int x, int y, string s) {
  SDL_Rect r;
  SDL_Texture* tex;
  get_text_and_rect(renderer, x, y, s.c_str(), font, &tex, &r);
  if (tex) {
    SDL_RenderCopy(renderer, tex, NULL, &r);
    SDL_DestroyTexture(tex);
  }
}



int main(int argc, char **argv) {

  printf("DEBUG: main() command-line arguments:\n");
  for (int i = 0; i < argc; ++i) {
    printf("%d: [%s]\n", i, argv[i]);
  }

  Verilated::commandArgs(argc, argv);
  // Verilated::traceEverOn(true);
  
  TB = new MAIN_TB();
#ifdef USE_POWER_PINS
  #pragma message "Howdy! This simulation build has USE_POWER_PINS in effect"
  TB->m_core->VGND = 0;
  TB->m_core->VPWR = 1;
#else
  #pragma message "Oh hi! USE_POWER_PINS is not in effect for this simulation build"
#endif
  uint8_t *framebuffer = new uint8_t[FRAMEBUFFER_SIZE];

  //SMELL: This needs proper error handling!
  printf("SDL_InitSubSystem(SDL_INIT_VIDEO): %d\n", SDL_InitSubSystem(SDL_INIT_VIDEO));

  SDL_Window* window =
      SDL_CreateWindow(
          " Verilator VGA simulation: " S2(VDESIGN),
          SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
          WINDOW_WIDTH, WINDOW_WIDTH,//WINDOW_HEIGHT,
          0
      );
  SDL_Renderer* renderer =
      SDL_CreateRenderer(
          window,
          -1,
          SDL_RENDERER_ACCELERATED
      );

  toggle_mouse_capture(true, gMouseCapture); // Dummy "toggle" to just set current mode, in order to print it.

  TTF_Init();
  TTF_Font *font = TTF_OpenFont(FONT_FILE, 12);
  if (!font) {
#if __cplusplus == 201703L
    std::filesystem::path font_path = std::filesystem::absolute(FONT_FILE);
#else
    string font_path = FONT_FILE;
#endif
    printf(
      "WARNING: Cannot load default font. Text rendering will be disabled.\n"
      "-- Looking for: %s\n",
      font_path.c_str()
    );
  }
  else {
    printf("Font loaded.\n");
  }

  SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);
  SDL_RenderClear(renderer);
  SDL_Texture* texture =
      SDL_CreateTexture(
          renderer,
          SDL_PIXELFORMAT_ARGB8888,
          SDL_TEXTUREACCESS_STREAMING,
          WINDOW_WIDTH, WINDOW_HEIGHT
      );

  printf(
    "\n"
    "Target clock speed: "
  );
  TB->print_big_num(CLOCK_HZ);
  printf(" Hz\n");

// #ifdef INSPECT_INTERNAL
//   printf(
//     "\n"
//     "Initial state of design:\n"
//     "  playerX  : %d\n"
//     "  playerY  : %d\n"
//     "  facingX  : %d\n"
//     "  facingY  : %d\n"
//     "  vplaneX  : %d\n"
//     "  vplaneY  : %d\n"
//     "\n",
//     TB->m_core->DESIGN->playerX,
//     TB->m_core->DESIGN->playerY,
//     TB->m_core->DESIGN->facingX,
//     TB->m_core->DESIGN->facingY,
//     TB->m_core->DESIGN->vplaneX,
//     TB->m_core->DESIGN->vplaneY
//   );
// #endif


  // printf("Starting simulation in ");
  // for (int c=3; c>0; --c) {
  //   printf("%i... ", c);
  //   fflush(stdout);
  //   sleep(1);
  // }
  printf("Cold start...\n");

  int h = 0;
  int v = 0;

  printf("Main loop...\n");

  gOriginalTime = gPrevTime = SDL_GetTicks();
  gPrevTickCount = TB->m_tickcount; // Used for measuring simulated clock speed.
  gPrevFrames = 0; // Used for calculating frame rate.
  Uint32 last_time = SDL_GetTicks(); // Used for calculating motion.

  bool count_hbp = false;
  int hbp_counter = 0; // Counter for timing the HBP (i.e. time after HSP, but before HDA).
  int h_adjust = HBP*2; // Amount to count in hbp_counter. Start at a high value and then sync back down.
  int h_adjust_countdown = REFRESH_FRAME*2;
  int v_shift = VBP*2; // This will try to find the vertical start of the image.

  while (!gQuit) {
    if (TB->done()) gQuit = true;
    if (TB->paused) SDL_WaitEvent(NULL); // If we're paused, an event is needed before we could resume.

    handle_control_inputs(true, 0); // true = PREPARE mode; set default signal inputs, so process_sdl_events can OPTIONALLY override.
    //SMELL: Should we do handle_control_inputs(true) only when we detect the start of a new frame,
    // so as to preserve/capture any keys that were pressed across *partial* refreshes?
    process_sdl_events();
    if (gQuit) break;
    if (TB->paused) continue;

    int old_reset = TB->m_core->rst_n;
    int time_delta = SDL_GetTicks() - last_time;
    last_time = SDL_GetTicks();
    handle_control_inputs(false, (double(time_delta)/1000.0)*60.0); // false = ACTIVE mode; add in actual HID=>signal input changes.
    if (old_reset != TB->m_core->rst_n || gDisplayResync) {
      // Resync needed, either explicitly or because reset state changed:
      gDisplayResync = false;
      h_adjust = HBP*2;
      count_hbp = false;
      hbp_counter = 0; // Counter for timing the HBP (i.e. time after HSP, but before HDA).
      h_adjust = HBP*2; // Amount to count in hbp_counter. Start at a high value and then sync back down.
      h_adjust_countdown = REFRESH_FRAME*2;
      v_shift = VBP*2; // This will try to find the vertical start of the image.
    }

    check_performance();

    clear_freshness(framebuffer);

    //SMELL: In my RTL, I call the time that comes before the horizontal display area the BACK porch,
    // even though arguably it comes first (so surely should be the FRONT), but this swapped naming
    // comes from other charts and diagrams I was reading online at the time.

    for (int i = 0; i < gRefreshLimit; ++i) {

      if (h_adjust_countdown > 0) --h_adjust_countdown;

      bool hsync_stopped = false;
      bool vsync_stopped = false;
      int hits = 0;
      TB->tick();      hsync_stopped |= TB->hsync_stopped();      vsync_stopped |= TB->vsync_stopped();

#ifdef USE_SPEAKER
      TB->examine_condition_met |= TB->m_core->speaker;
#endif // USE_SPEAKER

      if (hsync_stopped) {
        count_hbp = true;
        hbp_counter = 0;
      }

      int pixel_lit = TB->m_core->r | TB->m_core->g | TB->m_core->b;

      if (count_hbp) {
        // We are counting the HBP before we start the next line.
        if (hbp_counter >= h_adjust) {
          // OK, counter ran out, so let's start our next line.
          count_hbp = false;
          hbp_counter = 0;
          h = 0;
          v++;
        }
        else if (pixel_lit) {
          // If we got here, we got a display signal earlier than the current
          // horizontal adjustment expects, so we need to adjust HBP to match
          // HDA video signal, but only after the first full frame:
          if (h_adjust_countdown <= 0) {
            h_adjust = hbp_counter;
            printf(
              "[H,V,F=%4d,%4d,%2d] "
              "Horizontal auto-adjust to %d after HSYNC\n",
              h, v, TB->frame_counter,
              h_adjust
            );
          }
        }
        else {
          h++;
          hbp_counter++;
        }
      }
      else {
        h++;
      }

      if (vsync_stopped) {
        // Start a new frame.
        v = 0;
        // if (TB->frame_counter%60 == 0) overflow_test(framebuffer);
        fade_overflow_region(framebuffer);
      }

      if (pixel_lit && h_adjust_countdown <= 0 && v < v_shift) {
        v_shift = v;
        printf(
          "[H,V,F=%4d,%4d,%2d] "
          "Vertical frame auto-shift to %d after VSYNC\n",
          h, v, TB->frame_counter,
          v_shift
        );
        gSyncLine = true;
        gSyncFrame = true;
      }

      int x = h;
      int y = v;

#ifdef USE_SPEAKER
      int speaker = (TB->m_core->speaker<<6);
#else
      int speaker = 0;
#endif // USE_SPEAKER
      int hilite = gHighlight ? HILITE : 0; // hilite turns on lower 5 bits to show which pixel(s) have been updated.

      if (x >= 0 && x < WINDOW_WIDTH && y >= 0 && y < WINDOW_HEIGHT) {

        int red   = gRenderDAC ? TB->m_core->r : ((TB->m_core->r7 << 7) | (TB->m_core->r6 << 6));
        int green = gRenderDAC ? TB->m_core->g : ((TB->m_core->g7 << 7) | (TB->m_core->g6 << 6));
        int blue  = gRenderDAC ? TB->m_core->b : ((TB->m_core->b7 << 7) | (TB->m_core->b6 << 6));
        if (gDisableR) red = 0;
        if (gDisableG) green = 0;
        if (gDisableB) blue = 0;
        framebuffer[(y*WINDOW_WIDTH + x)*4 + 2] = red   | (TB->m_core->hsync ? 0 : 0b1000'0000) | speaker;  // R
        framebuffer[(y*WINDOW_WIDTH + x)*4 + 1] = green;                                                    // G
        framebuffer[(y*WINDOW_WIDTH + x)*4 + 0] = blue  | (TB->m_core->vsync ? 0 : 0b1000'0000) | speaker;  // B.
      }

      if (gSyncLine && h==0) {
        gSyncLine = false;
        break;
      }

      if (gSyncFrame && v==0) {
        gSyncFrame = false;
        break;
      }

    }

    overlay_display_area_frame(framebuffer, 0, v_shift);

    SDL_UpdateTexture( texture, NULL, framebuffer, WINDOW_WIDTH * 4 );
    SDL_Rect dr;
    dr.x = 0; dr.y = 100;
    dr.w = WINDOW_WIDTH; dr.h = WINDOW_HEIGHT;
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
    SDL_RenderFillRect(renderer, NULL);
    if (gRotateView) {
      // Rotated orientation.
      SDL_RenderCopyEx( renderer, texture, NULL, &dr, -90, NULL, SDL_FLIP_NONE );
    } else {
      // Normal orientation.
      SDL_RenderCopy( renderer, texture, NULL, &dr );
    }

// #ifdef INSPECT_INTERNAL
//     printf("%06X %06X %06X %06X %06X %06X\n",
//       TB->m_core->DESIGN->playerX,
//       TB->m_core->DESIGN->playerY,
//       TB->m_core->DESIGN->facingX,
//       TB->m_core->DESIGN->facingY,
//       TB->m_core->DESIGN->vplaneX,
//       TB->m_core->DESIGN->vplaneY
//     );
// #endif//INSPECT_INTERNAL
    if (font) {
      SDL_Rect rect;
      SDL_Texture *text_texture = NULL;
      // Show the state of controls that can be toggled:
      string s = "[";
      s += TB->paused           ? "P" : ".";
      s += gGuides              ? "G" : ".";
      s += gHighlight           ? "H" : ".";
      // s += TB->log_vsync        ? "V" : ".";
      // s += gOverrideVectors     ? "O" : ".";
      // s += TB->examine_mode     ? "X" : ".";
      // s += gLockInputs[LOCK_MAP]? "m" : ".";
      s += gLockInputs[LOCK_DEBUG]? "D" : ".";
    #ifdef DESIGN_DIRECT_VECTOR_ACCESS
      s += gLockInputs[LOCK_L]  ? "<" : ".";
      s += gLockInputs[LOCK_F]  ? "^" : ".";
      s += gLockInputs[LOCK_B]  ? "v" : ".";
      s += gLockInputs[LOCK_R]  ? ">" : ".";
    #endif
      s += gMouseCapture        ? "*" : ".";
      s += "] ";
      s += "ui_in: ";
      int uii = TB->m_core->ui_in;
      for (int b = 0; b<8; ++b) {
        s += (uii & 0x80) ? "1" : "0";
        if (b==3) s+= "'";
        uii <<= 1;
      }

#ifdef INSPECT_INTERNAL
      s += " pX,Y=("
        + to_string(fixed2double(TB->m_core->DESIGN->playerX)) + ", "
        + to_string(fixed2double(TB->m_core->DESIGN->playerY)) + ") ";
      s += " fX,Y=("
        + to_string(fixed2double(TB->m_core->DESIGN->facingX)) + ", "
        + to_string(fixed2double(TB->m_core->DESIGN->facingY)) + ") ";
      s += " vX,Y=("
        + to_string(fixed2double(TB->m_core->DESIGN->vplaneX)) + ", "
        + to_string(fixed2double(TB->m_core->DESIGN->vplaneY)) + ") ";
      s += " sf=" + to_string(gView.sf);
      s += " sv=" + to_string(gView.sv);
#endif//INSPECT_INTERNAL
      get_text_and_rect(renderer, 10, 10, s.c_str(), font, &text_texture, &rect);
      if (text_texture) {
        SDL_RenderCopy(renderer, text_texture, NULL, &rect);
        SDL_DestroyTexture(text_texture);
      }
      else {
        printf("Cannot create text_texture\n");
      }
    }
    SDL_RenderPresent(renderer);
  }

  SDL_DestroyRenderer(renderer);
  SDL_DestroyWindow(window);
  SDL_Quit(); //SMELL: Should use SDL_QuitSubSystem instead? https://wiki.libsdl.org/SDL2/SDL_QuitSubSystem
  if (font) TTF_CloseFont(font);
  TTF_Quit();

  delete framebuffer;

  printf("Done at %lu ticks.\n", TB->m_tickcount);
  return EXIT_SUCCESS;
}
