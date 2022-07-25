import React,{useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import Container from 'react-bootstrap/Container';
const templatePict = require('./lenna.png');

const Main = () => {
  const [pict, setPict] = useState(templatePict);

  const changePict = (e) => {
    setPict(URL.createObjectURL(e.target.files[0]));
  }
  return (
    <main style={{justifyContent:'center'}}>
      <Form.Group>
        <Form.Label>Image To Change</Form.Label>      
          <FormControl type="file" onChange={changePict}/>
      </Form.Group>
      <Container fluid className="d-flex mt-3 justify-content-center" style={{maxHeight:'80%'}}>
        <img src={pict} alt="Picture" />
      </Container>
    </main>
  );
};

export default Main;