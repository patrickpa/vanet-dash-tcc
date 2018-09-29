//
// Copyright (C) 2006-2017 Christoph Sommer <sommer@ccs-labs.org>
//
// Documentation for these modules is at http://veins.car2x.org/
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 2 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
//

package vanet_dash_v_0_1.simulations;

import inet.networklayer.configurator.ipv4.IPv4NetworkConfigurator;
import inet.node.inet.AdhocHost;
import inet.node.inet.INetworkNode;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
import inet.node.inet.WirelessHost;
import inet.node.internetcloud.InternetCloud;
import inet.node.wireless.AccessPoint;
import inet.physicallayer.idealradio.IdealRadioMedium;
import inet.visualizer.contract.IIntegratedVisualizer;
import inet.node.aodv.AODVRouter;
import inet.common.lifecycle.LifecycleController;
import inet.common.scenario.ScenarioManager;
import inet.networklayer.configurator.ipv4.IPv4NetworkConfigurator;
import inet.networklayer.ipv4.RoutingTableRecorder;
import inet.node.aodv.AODVRouter;
import inet.physicallayer.idealradio.IdealRadioMedium;
import inet.physicallayer.ieee80211.packetlevel.Ieee80211ScalarRadioMedium;
import inet.visualizer.integrated.IntegratedCanvasVisualizer;
import org.car2x.veins.nodes.Car;
import org.car2x.veins.subprojects.veins_inet.VeinsInetManager;

network Scenario_dash
{
    parameters:
        @display("bgb=545,515");
        string mediumType = default("IdealRadioMedium");
    submodules:
        radioMedium: IdealRadioMedium;
        manager: VeinsInetManager;
        node[0]: org.car2x.veins.subprojects.veins_inet.example.Car {
            @display("p=38,143");
        }
        configurator: IPv4NetworkConfigurator {
            parameters:
                @display("p=201,39");
        }

        host5G_server: org.car2x.veins.subprojects.veins_inet.example.Car {
            @display("p=179,229");
        }
}
