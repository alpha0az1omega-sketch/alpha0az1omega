// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract AlphaLicense {
    string public projectName = "alpha0az1omega";
    string public pgpFingerprint = "643F45B7B3A9C65C1DB1703B9870EEC405078488";
    address public creator;
    
    // THE LINK: We store the hash of the CORE (Rust/WASM) to bind logic and value
    string public coreMathHash; 

    uint256 public royaltyBasisPoints = 500; 

    event LicensePurchased(address indexed buyer, uint256 amountPaid);

    // The constructor now requires the hash of the CORE to initialize
    constructor(string memory _coreMathHash) {
        creator = msg.sender;
        coreMathHash = _coreMathHash;
    }

    function purchaseLicense() external payable {
        require(msg.value > 0, "Must send some ETH to purchase a license");
        (bool success, ) = creator.call{value: msg.value}("");
        require(success, "Transfer to creator failed");
        emit LicensePurchased(msg.sender, msg.value);
    }

    function getIdentity() external view returns (string memory) {
        return pgpFingerprint;
    }
}
