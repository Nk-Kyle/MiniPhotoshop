import React, {useState} from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';
import ButtonGroup from 'react-bootstrap/ButtonGroup';

const Main = ({pict, setPict, undo, setUndo, redo, setRedo, loading}) => {
  const [basePict, setBasePict] = useState('');
  const addPict = async (e) => {
    const file = e.target.files[0];
    const base64 = await toBase64(file);
    setPict(base64);
    setBasePict(base64);
    setUndo([]);
    setRedo([]);
  }

  const toBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const fileReader = new FileReader();
      fileReader.readAsDataURL(file);

      fileReader.onload = () => resolve(fileReader.result);
      fileReader.onerror = (error) => reject(error);
    })
  }

  const undoChanges = () => {
    if (undo.length > 0 && !loading) {
      setPict(undo[undo.length - 1]);
      setUndo(undo.slice(0, undo.length - 1));
      setRedo([pict,...redo])
    }
  }

  const resetChanges = () => {
    if (!loading) {
      setPict(basePict);
      setUndo([]);
      setRedo([]);
    }
  }

  const redoChanges = () => {
    if (redo.length > 0 && !loading) {
      setPict(redo[0]);
      setRedo(redo.slice(1));
      setUndo([...undo, pict]);
    }
  }

  return (
    <main style={{justifyContent:'center'}}>
      <Form.Group>
        <Form.Label>Image To Change</Form.Label>      
          <FormControl type="file" onChange={(e) => addPict(e) }/>
      </Form.Group>
      <ButtonGroup aria-label="Basic example" className="mt-3">
        <Button variant="outline-primary" onClick={undoChanges}>Undo</Button>
        <Button variant="outline-primary" onClick={resetChanges}>Reset</Button>
        <Button variant="outline-primary" onClick={redoChanges}>Redo</Button>
      </ButtonGroup>
      <Container fluid className="d-flex mt-3 justify-content-center" style={{maxHeight:'80%', maxWidth : '100%'}}>
        <img src={pict} alt="" />
      </Container>
      {
        pict !== '' ?
         <Button variant="outline-dark mt-3" href={loading ? '' : pict} download={'photoshop_result'}>{loading? 'Loading' : 'Download'}</Button>
        :
        <></>
      }
    </main>
  );
};

export default Main;