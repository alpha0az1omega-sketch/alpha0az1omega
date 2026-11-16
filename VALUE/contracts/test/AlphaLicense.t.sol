// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {AlphaLicense} from "../src/AlphaLicense.sol";

contract AlphaLicenseTest is Test {
    AlphaLicense public license;
    address public buyer = address(0x123);
    address public creator = makeAddr("creator");

    function setUp() public {
        vm.prank(creator);
        // We pass the mock hash here as well
        license = new AlphaLicense("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855");
    }

    function testIdentityMatchesPGP() public view {
        assertEq(license.getIdentity(), "643F45B7B3A9C65C1DB1703B9870EEC405078488");
    }

    function testPurchaseLicense() public {
        vm.deal(buyer, 1 ether);
        uint256 creatorBalanceBefore = creator.balance;
        
        vm.prank(buyer);
        license.purchaseLicense{value: 0.1 ether}();
        
        assertEq(creator.balance, creatorBalanceBefore + 0.1 ether);
    }
}
