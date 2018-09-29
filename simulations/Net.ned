//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
// 
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
// 
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
// 

package vanet_dash_v_0_1.simulations;

import inet.networklayer.configurator.ipv4.IPv4NetworkConfigurator;
import inet.node.inet.AdhocHost;
import inet.node.inet.INetworkNode;
import inet.node.inet.Router;
import inet.node.inet.StandardHost;
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

network Net
{
    parameters:
        int numHosts;
        string hostType = default("AODVRouter");
        string mediumType = default("IdealRadioMedium");
        @display("bgb=1000,700");

    submodules:
        visualizer: <default("IntegratedCanvasVisualizer")> like IIntegratedVisualizer if hasVisualizer() {
            parameters:
                @display("p=61.1,14.3");
        }
        configurator: IPv4NetworkConfigurator {
            parameters:
                @display("p=61.1,127.4");
        }
        radioMedium: IdealRadioMedium {
            parameters:
                @display("p=59.8,67.6");
        }
        hostA: AODVRouter {
            @display("i=device/pocketpc_s;p=782.86206,544.9101");
        }
        hostB: AODVRouter {
            @display("i=device/pocketpc_s;p=145.15071,242.71104");
        }
        hostR[numHosts]: AODVRouter {
            parameters:
                @display("i=device/pocketpc_s;r=,,#707070;");
        }

}
