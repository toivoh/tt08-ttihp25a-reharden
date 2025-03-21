/*  This file is part of Gatery, a library for circuit design.
	Copyright (C) 2021 Michael Offel, Andreas Ley

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
#include "gatery/scl_pch.h"
#include "TileLinkDMA.h"

namespace gtry::scl
{
	void tileLinkFromStream(RvStream<AxiToStreamCmd>&& cmd, RvStream<BVec>&& data, TileLinkUB&& slave)
	{
		Area ent{ "scl_tileLinkFromStream", true };

		AxiConfig axiCfg{ 
			.addrW = slave.a->address.width(),
			.dataW = slave.a->data.width(),
		};
		RvStream<AxiAddress> cmdAddr = axiGenerateAddressFromCommand(std::move(cmd), axiCfg);
		ready(cmdAddr) = transfer(slave.a) & eop(slave.a);
		ready(data) = ready(slave.a);
		ready(*slave.d) = '1';

		valid(slave.a) = valid(cmdAddr) & valid(data);
		slave.a->setupPut(cmdAddr->addr, *data, (UInt)cmd->id, utils::Log2C(cmd->bytesPerBurst));
	}
}
