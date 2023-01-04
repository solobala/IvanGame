import React, { Component } from 'react';
import CustomersService from './OwnersService';

const ownersService = new OwnersService();

class OwnerCreateUpdate extends Component {
    constructor(props) {
        super(props);

        this.handleSubmit = this.handleSubmit.bind(this);
      }

      componentDidMount(){
        const { match: { params } } = this.props;
        if(params && params.pk)
        {
          ownersService.getOwner(params.pk).then((o)=>{
            this.refs.ownerName.value = o.owner_name;
            this.refs.ownerDescription.value = o.owner_description;
            this.refs.link.value = o.link;
            this.refs.ownerImg.value = o.owner_img;
            this.refs.status.value = o.status;

        }
      }

      handleCreate(){
        ownersService.createOwner(
          {
            "owner_name": this.refs.ownerName.value,
            "owner_description": this.refs.ownerDescription.value,
            "link": this.refs.link.value,
            "owner_img": this.refs.ownerImg.value,
            "status": this.refs.status.value,

        }
        ).then((result)=>{
          alert("Профиль игрока создан!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleUpdate(pk){
        ownersService.updateOwner(
          {
            "pk": pk,
            "owner_name": this.refs.ownerName.value,
            "owner_description": this.refs.ownerDescription.value,
            "link": this.refs.link.value,
            "owner_img": this.refs.ownerImg.value,
            "status": this.refs.status.value,

        }
        ).then((result)=>{
          console.log(result);
          alert("Профиль Игрока обновлен!");
        }).catch(()=>{
          alert('There was an error! Please re-check your form.');
        });
      }
      handleSubmit(event) {
        const { match: { params } } = this.props;

        if(params && params.pk){
          this.handleUpdate(params.pk);
        }
        else
        {
          this.handleCreate();
        }

        event.preventDefault();
      }

      render() {
        return (
          <form onSubmit={this.handleSubmit}>
          <div className="form-group">
            <label>
              Игрок:</label>
              <input className="form-control" type="text" ref='ownerName' />

            <label>
              Описание:</label>
              <textarea className="form-control" ref='ownerDescription' ></textarea>

            <label>
              Ссылка:</label>
              <input className="form-control" type="text" ref='link' />

            <label>
              Изображение:</label>
              <input className="form-control" type="text" ref='ownerImg' />

            <label>
              Статус:</label>
              <input className="form-control" type="img" ref='status' />

            <input className="btn btn-primary" type="submit" value="Submit" />
            </div>
          </form>
        );
      }
}

export default OwnerCreateUpdate;