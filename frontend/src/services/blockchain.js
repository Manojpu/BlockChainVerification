import Web3 from 'web3';
import ResumeVerifier from '../../smart-contracts/contracts/ResumeVerifier.json';

let web3;
let contract;

const initWeb3 = async () => {
    if (window.ethereum) {
        web3 = new Web3(window.ethereum);
        await window.ethereum.request({ method: 'eth_requestAccounts' });
    } else {
        console.error('Please install MetaMask!');
    }
};

const initContract = () => {
    const networkId = Object.keys(ResumeVerifier.networks)[0];
    contract = new web3.eth.Contract(
        ResumeVerifier.abi,
        ResumeVerifier.networks[networkId].address
    );
};

const uploadResume = async (resumeData) => {
    const accounts = await web3.eth.getAccounts();
    const result = await contract.methods.uploadResume(resumeData).send({ from: accounts[0] });
    return result;
};

const verifyResume = async (resumeHash) => {
    const result = await contract.methods.verifyResume(resumeHash).call();
    return result;
};

export { initWeb3, initContract, uploadResume, verifyResume };