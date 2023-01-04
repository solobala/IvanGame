import React, { Component } from "react";
import { Col, Container, Row } from "reactstrap";
import StudentList from "./OwnerList";
import NewStudentModal from "./NewOwnerModal";

import axios from "axios";

import { API_URL } from "../constants";

class Home extends Component {
  state = {
    owners: []
  };

  componentDidMount() {
    this.resetState();
  }

  getOwners = () => {
    axios.get(API_URL).then(res => this.setState({ owners: res.data }));
  };

  resetState = () => {
    this.getOwners();
  };

  render() {
    return (
      <Container style={{ marginTop: "20px" }}>
        <Row>
          <Col>
            <OwnerList
              owners={this.state.owners}
              resetState={this.resetState}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <NewOwnerModal create={true} resetState={this.resetState} />
          </Col>
        </Row>
      </Container>
    );
  }
}

export default Home;