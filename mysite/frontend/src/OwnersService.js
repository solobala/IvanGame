import axios from './axios';
const API_URL = 'http://localhost:8000';

export default class OwnersService{

	constructor(){}


	getCustomers() {
		const url = `${API_URL}/poll/owners/`;
		return axios.get(url).then(response => response.data);
	}
	getOwnersByURL(link){
		const url = `${API_URL}${link}`;
		return axios.get(url).then(response => response.data);
	}
	getOwner(pk) {
		const url = `${API_URL}/poll/owners/${pk}`;
		return axios.get(url).then(response => response.data);
	}
	deleteOwner(owner){
		const url = `${API_URL}/poll/owners/${owner.pk}`;
		return axios.delete(url);
	}
	createOwner(owner){
		const url = `${API_URL}/poll/owners/`;
		return axios.post(url,owner);
	}
	updateOwner(owner){
		const url = `${API_URL}/poll/owners/${owner.pk}`;
		return axios.put(url,owner);
	}
}