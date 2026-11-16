// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/**
 * @title AlphaLicense
 * @dev The Economic Organ of the alpha0az1omega repository.
 * It binds a license to a specific PGP identity fingerprint.
 */
contract AlphaLicense {
    string public projectName = "alpha0az1omega";
    string public pgpFingerprint = "643F45B7B3A9C65C1DB1703B9870EEC405078488";
    address public creator;
    
    // The royalty fee in basis points (e.g., 500 = 5%)
    uint256 public royaltyBasisPoints = 500; 

    event LicensePurchased(address indexed buyer, uint256 amountPaid);

    constructor() {
        // The deployer of the contract is the creator
        creator = msg.sender;
    }

    /**
     * @dev Allows someone to purchase a license to use the code.
     * The funds are sent directly to the creator.
     */
    function purchaseLicense() external payable {
        require(msg.value > 0, "Must send some ETH to purchase a license");
        
        (bool success, ) = creator.call{value: msg.value}("");
        require(success, "Transfer to creator failed");
        
        emit LicensePurchased(msg.sender, msg.value);
    }

    /**
     * @dev Returns the cryptographic identity of the contract's owner.
     */
    function getIdentity() external view returns (string memory) {
        return pgpFingerprint;
    }
}
