// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {AlphaLicense} from "../src/AlphaLicense.sol";

contract AlphaLicenseTest is Test {
    AlphaLicense public license;
    address public buyer = address(0x123);
    // We create a dedicated address for the creator to receive funds
    address public creator = makeAddr("creator");

    function setUp() public {
        // We deploy the contract AS the creator
        vm.prank(creator);
        license = new AlphaLicense();
    }

    function testIdentityMatchesPGP() public view {
        assertEq(license.getIdentity(), "643F45B7B3A9C65C1DB1703B9870EEC405078488");
    }

    function testPurchaseLicense() public {
        vm.deal(buyer, 1 ether);
        
        uint256 creatorBalanceBefore = creator.balance;
        
        // The buyer purchases the license
        vm.prank(buyer);
        license.purchaseLicense{value: 0.1 ether}();
        
        // We assert that the creator actually received the 0.1 ETH
        assertEq(creator.balance, creatorBalanceBefore + 0.1 ether);
    }
}
