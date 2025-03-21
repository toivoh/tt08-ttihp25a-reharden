/*  This file is part of Gatery, a library for circuit design.
	Copyright (C) 2022 Michael Offel, Andreas Ley

	Gatery is free software; you can redistribute it and/or
	modify it under the terms of the GNU Lesser General Public
	License as published by the Free Software Foundation; either
	version 3 of the License, or (at your option) any later version.

	Gatery is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
	Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public
	License along with this library; if not, write to the Free Software
	Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
*/
#pragma once


#include "../../compat/CoroutineWrapper.h"

namespace gtry::hlim {
	class Clock;
}

namespace gtry::sim {

/**
 * @brief co_awaiting on a WaitStable continues the simulation until the signal states for a simulation time step and phase have stabilized (the last micro tick).
 */
class WaitStable {
	public:
		WaitStable();

		bool await_ready() noexcept { return false; } // always force reevaluation
		void await_suspend(std::coroutine_handle<> handle);
		void await_resume() noexcept { }
	protected:
};

}
