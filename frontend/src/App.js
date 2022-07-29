import React,{useState} from 'react';
import 'react-pro-sidebar/dist/css/styles.css';
import Aside from './Aside';
import Main from './Main';
import './styles/App.scss';

function App() {
  const [pict, setPict] = useState('');
  const [undo, setUndo] = useState([]);
  const [redo, setRedo] = useState([]);
  const [loading, setLoading] = useState(false);

  return (
    <div className='app'>
      <Aside setPict={setPict} setUndo={setUndo} setRedo = {setRedo} pict={pict} undo = {undo} loading = {loading} setLoading={setLoading}/>
      <Main pict = {pict} setPict = {setPict} undo = {undo} setUndo = {setUndo} redo = {redo} setRedo = {setRedo} loading = {loading}/>
    </div>
  );
}

export default App;

