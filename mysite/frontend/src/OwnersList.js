import  React, { Component } from  'react';
import  OwnersService  from  './OwnersService';

const  ownersService  =  new  OwnersService();

class  OwnersList  extends  Component {

constructor(props) {
	super(props);
	this.state  = {
		owners: [],
		nextPageURL:  ''
	};
	this.nextPage  =  this.nextPage.bind(this);
	this.handleDelete  =  this.handleDelete.bind(this);
}

componentDidMount() {
	var  self  =  this;
	ownersService.getOwners().then(function (result) {
		console.log(result);
		self.setState({ owners:  result.data, nextPageURL:  result.nextlink})
	});
}
handleDelete(e,pk){
	var  self  =  this;
	ownersService.deleteOwner({pk :  pk}).then(()=>{
		var  newArr  =  self.state.owners.filter(function(obj) {
			return  obj.pk  !==  pk;
		});

		self.setState({owners:  newArr})
	});
}

nextPage(){
	var  self  =  this;
	console.log(this.state.nextPageURL);
	ownersService.getOwnersByURL(this.state.nextPageURL).then((result) => {
		self.setState({ owners:  result.data, nextPageURL:  result.nextlink})
	});
}
render() {

	return (
		<div  className="owners--list">
			<table  className="table">
			<thead  key="thead">
			<tr>
				<th>#</th>
				<th>Игрок</th>
				<th>Описание</th>
				<th>Ссылка</th>
				<th>Изображение</th>
				<th>Статус</th>

			</tr>
			</thead>
			<tbody>
			{this.state.owners.map( o  =>
				<tr  key={o.pk}>
				<td>{o.pk}  </td>
				<td>{o.owner_name}</td>
				<td>{o.owner_description}</td>
				<td>{o.link}</td>
				<td>{o.owner_img}</td>
				<td>{o.status}</td>

				<td>
				<button  onClick={(e)=>  this.handleDelete(e,o.pk) }> Delete</button>
				<a  href={"/owner/" + o.pk}> Update</a>
				</td>
			</tr>)}
			</tbody>
			</table>
			<button  className="btn btn-primary"  onClick=  {  this.nextPage  }>Next</button>
		</div>
		);
  }
}
export  default  OwnersList;