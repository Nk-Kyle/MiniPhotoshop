import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import Container from 'react-bootstrap/Container';


const Main = ({pict, setPict}) => {
  const setBasePict = (e) => {
  }
  return (
    <main style={{justifyContent:'center'}}>
      <Form.Group>
        <Form.Label>Image To Change</Form.Label>      
          <FormControl type="file" onChange={(e) => { setPict(URL.createObjectURL(e.target.files[0])) } }/>
      </Form.Group>
      <Container fluid className="d-flex mt-3 justify-content-center" style={{maxHeight:'80%'}}>
        <img src={pict} alt="" />
      </Container>
    </main>
  );
};

export default Main;