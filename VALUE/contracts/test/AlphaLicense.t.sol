// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Test} from "forge-std/Test.sol";
import {AlphaLicense} from "../src/AlphaLicense.sol";

contract AlphaLicenseTest is Test {
    AlphaLicense public license;
    address public buyer = address(0x123);
    address public creator = makeAddr("creator");
    address public royaltyRecipient = makeAddr("royalty");

    function setUp() public {
        vm.prank(creator);
        license = new AlphaLicense("e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", royaltyRecipient);
    }

    function testIdentityMatchesPGP() public view {
        assertEq(license.getIdentity(), "27D7D0E98A47D4A27124CC53EEC3D5AE9D2E2290");
    }

    function testRoyaltiesSplit() public {
        vm.deal(buyer, 1 ether);
        
        uint256 creatorBalanceBefore = creator.balance;
        uint256 royaltyBalanceBefore = royaltyRecipient.balance;
        
        // Buyer purchases for 1 ETH
        vm.prank(buyer);
        license.purchaseLicense{value: 1 ether}();
        
        // 5% of 1 ETH = 0.05 ETH. Creator gets 0.95 ETH.
        assertEq(creator.balance, creatorBalanceBefore + 0.95 ether);
        assertEq(royaltyRecipient.balance, royaltyBalanceBefore + 0.05 ether);
    }
}
