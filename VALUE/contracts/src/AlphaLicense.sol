// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract AlphaLicense {
    string public projectName = "alpha0az1omega";
    // CORRECTION F4 : Nouvelle empreinte PGP
    string public pgpFingerprint = "27D7D0E98A47D4A27124CC53EEC3D5AE9D2E2290";
    
    address public creator;
    address public royaltyRecipient;
    
    // CORRECTION F5 : Implémentation des royalties (5%)
    uint256 public royaltyBasisPoints = 500; // 5%
    uint256 public constant BASIS_POINTS_DENOMINATOR = 10000;
    
    string public coreMathHash; 

    event LicensePurchased(address indexed buyer, uint256 amountPaid, uint256 royaltyPaid);

    // CORRECTION F7 : Protection contre la réentrance
    uint256 private _status = 1;
    modifier nonReentrant() {
        require(_status != 2, "ReentrancyGuard: reentrant call");
        _status = 2;
        _;
        _status = 1;
    }

    constructor(string memory _coreMathHash, address _royaltyRecipient) {
        creator = msg.sender;
        royaltyRecipient = _royaltyRecipient;
        coreMathHash = _coreMathHash;
    }

    function purchaseLicense() external payable nonReentrant {
        require(msg.value > 0, "Must send some ETH to purchase a license");
        
        uint256 royaltyAmount = (msg.value * royaltyBasisPoints) / BASIS_POINTS_DENOMINATOR;
        uint256 creatorAmount = msg.value - royaltyAmount;
        
        // Payer le créateur
        (bool successCreator, ) = creator.call{value: creatorAmount}("");
        require(successCreator, "Transfer to creator failed");
        
        // Payer les royalties
        if (royaltyAmount > 0 && royaltyRecipient != address(0)) {
            (bool successRoyalty, ) = royaltyRecipient.call{value: royaltyAmount}("");
            require(successRoyalty, "Transfer to royalty recipient failed");
        }

        emit LicensePurchased(msg.sender, msg.value, royaltyAmount);
    }

    function getIdentity() external view returns (string memory) {
        return pgpFingerprint;
    }
}
