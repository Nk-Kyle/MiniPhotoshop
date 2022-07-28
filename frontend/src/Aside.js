import React from 'react';
import {
  ProSidebar,
  Menu,
  MenuItem
} from 'react-pro-sidebar';
import {FaGem} from 'react-icons/fa';

const Aside = ({setPict, setUndo, setRedo}) => {
  return (
    <ProSidebar breakPoint='md'>
        <Menu iconShape="square">
            <MenuItem icon={<FaGem />}>Dashboard</MenuItem>
        </Menu>
    </ProSidebar>
  );
};

export default Aside;