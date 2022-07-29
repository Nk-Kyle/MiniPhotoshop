import React,{useState} from 'react';
import 'react-pro-sidebar/dist/css/styles.css';
import Aside from './Aside';
import Main from './Main';
import './styles/App.scss';

function App() {
  const [pict, setPict] = useState([]);
  const [undo, setUndo] = useState([]);
  const [redo, setRedo] = useState([]);


  return (
    <div className='app'>
      <Aside setPict={setPict} setUndo={setUndo} setRedo = {setRedo} pict={pict} undo = {undo} redo = {redo}/>
      <Main pict = {pict} setPict = {setPict} undo = {undo} setUndo = {setUndo} redo = {redo} setRedo = {setRedo} />
    </div>
  );
}

export default App;

