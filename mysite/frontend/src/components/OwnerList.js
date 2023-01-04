import React, { Component } from "react";
import { Table } from "reactstrap";
import NewOwnerModal from "./NewOwnerModal";

import ConfirmRemovalModal from "./ConfirmRemovalModal";

class OwnerList extends Component {
  render() {
    const owners = this.props.owners;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Link</th>
            <th>Picture</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!owners || owners.length <= 0 ? (
            <tr>
              <td colSpan="6" align="center">
                <b>Ops, no one here yet</b>
              </td>
            </tr>
          ) : (
            owners.map(owner => (
              <tr key={student.pk}>
                <td>{owner.owner_name}</td>
                <td>{owner.owner_description}</td>
                <td>{owner.link}</td>
                <td>{owner.owner_img}</td>
                <td>{owner.status}</td>
                <td align="center">
                  <NewOwnerModal
                    create={false}
                    owner={owner}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    pk={owner.pk}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default OwnerList;