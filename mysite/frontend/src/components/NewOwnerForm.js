import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";

import axios from "axios";

import { API_URL } from "../constants";

class NewOwnerForm extends React.Component {
  state = {
    pk: 0,
    owner_name: "",
    owner_description: "",
    link: "",
    owner_img: "",
    status: ""
  };

  componentDidMount() {
    if (this.props.student) {
      const { pk, owner_name, owner_description, link, owner_img,status } = this.props.owner;
      this.setState({ pk, owner_name, owner_description, link, owner_img,status });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createStudent = e => {
    e.preventDefault();
    axios.post(API_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editStudent = e => {
    e.preventDefault();
    axios.put(API_URL + this.state.pk, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.student ? this.editStudent : this.createStudent}>
        <FormGroup>
          <Label for="owner_name">Name:</Label>
          <Input
            type="text"
            name="owner_name"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.owner_name)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="owner_description">Description:</Label>
          <Input
            type="TextArea"
            name="owner_description"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.owner_description)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="link">Link:</Label>
          <Input
            type="text"
            name="link"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.link)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="owner_img">Picture:</Label>
          <Input
            type="file"
            name="owner_img"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.owner_img)}
          />
        </FormGroup>
          <FormGroup>
          <Label for="status">Status:</Label>
          <Input
            type="select"
            name="status"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.status)}
          />
        </FormGroup>
        <Button>Send</Button>
      </Form>
    );
  }
}

export default NewOwnerForm;