import React from 'react'; 
import {
  ProSidebar,
  Menu,
  MenuItem
} from 'react-pro-sidebar';
import {GrRotateRight, GrRotateLeft} from 'react-icons/gr';
import {GiHorizontalFlip, GiVerticalFlip} from 'react-icons/gi';
import {AiOutlineZoomIn, AiOutlineZoomOut,AiFillMinusCircle,AiOutlineFieldBinary, AiOutlineBorder} from 'react-icons/ai';
import {BsFillBrightnessHighFill} from 'react-icons/bs';
import {ImContrast} from 'react-icons/im';
import {MdDarkMode, MdLensBlur} from 'react-icons/md';
import {BsArrow90DegDown,BsArrow90DegUp} from 'react-icons/bs';
import {CgEditNoise} from 'react-icons/cg';


const Aside = ({setPict, setUndo, setRedo, pict, undo, loading, setLoading}) => {

  const requestApi = async (url) => {
    if (!loading) {
      setLoading(true);
      try{
        if (pict !== '') {
          const response = await fetch("http://127.0.0.1:8000/api/"+url+"/", {
            method: 'POST',
            body: JSON.stringify({
              "pict": pict
            }),
            headers: {
              'Content-Type': 'application/json'
            }
          });
          if (!response.ok) {
            throw new Error(`Error! status: ${response.status}`);
          }

          const result = await response.json();
          setUndo([...undo, pict])
          setRedo([])
          setPict(result.res)
        }
      } catch (error) {}
      finally {
        setLoading(false);
      }
    }
    else {
      console.log('Another request is in progress');
    }
  };

  return (
    <ProSidebar breakPoint='md'>
        <Menu iconShape="square">
            <MenuItem icon={<AiFillMinusCircle /> } onClick= {() => requestApi("negative")}>Negative</MenuItem>
            <MenuItem icon={<MdDarkMode /> } onClick= {() => requestApi("grayScale")}>GrayScale</MenuItem>
            <MenuItem icon={<AiOutlineFieldBinary /> } onClick= {() => requestApi("complement")}>Complement</MenuItem>
            <MenuItem icon={<GrRotateRight /> } onClick= {() => requestApi("rotateRight")}>Rotate CW</MenuItem>
            <MenuItem icon={<GrRotateLeft />} onClick= {() => requestApi("rotateLeft")}>Rotate CCW</MenuItem>
            <MenuItem icon={<GiHorizontalFlip />} onClick= {() => requestApi("horizontalFlip")}>Flip Horizontal</MenuItem>
            <MenuItem icon={<GiVerticalFlip />} onClick={() => requestApi("verticalFlip")}>Flip Vertical</MenuItem>
            <MenuItem icon={<AiOutlineZoomIn />} onClick={() => requestApi("zoomIn")}>Zoom In</MenuItem>
            <MenuItem icon={<AiOutlineZoomOut />} onClick={() => requestApi("zoomOut")}>Zoom Out</MenuItem>
            <MenuItem icon={<BsFillBrightnessHighFill />}onClick={() => requestApi("brighten")}>Brighten Image</MenuItem>
            <MenuItem icon={<ImContrast />}onClick={() => requestApi("contrast")}>Contrast Image</MenuItem>
            <MenuItem icon={<BsArrow90DegDown />}onClick={() => requestApi("log")}>Log Transform</MenuItem>
            <MenuItem icon={<BsArrow90DegUp />}onClick={() => requestApi("exp")}>Exponential Transform</MenuItem>
            <MenuItem icon={<MdLensBlur />}onClick={() => requestApi("gaussianBlur")}>Blur Image</MenuItem>
            <MenuItem icon={<AiOutlineBorder />}onClick={() => requestApi("gaussianSharpening")}>Sharpen Image</MenuItem>
            <MenuItem icon={<CgEditNoise />}onClick={() => requestApi("addNoise")}>Add Noise</MenuItem>
            

        </Menu>
    </ProSidebar>
  );
};

export default Aside;