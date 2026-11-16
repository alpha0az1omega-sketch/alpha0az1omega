// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script} from "forge-std/Script.sol";
import {console} from "forge-std/console.sol";
import {AlphaLicense} from "../src/AlphaLicense.sol";

contract Deploy is Script {
    function run() external {
        // We use the default Anvil private key to deploy locally
        uint256 deployerPrivateKey = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80;
        
        vm.startBroadcast(deployerPrivateKey);
        
        // We pass the mock hash to bind the CORE and VALUE
        AlphaLicense license = new AlphaLicense("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
        
        vm.stopBroadcast();
        
        // Log the deployed contract address
        console.log("AlphaLicense deployed at:", address(license));
    }
}
