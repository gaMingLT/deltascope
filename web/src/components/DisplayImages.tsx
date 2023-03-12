import { Alert, Box, Button } from "@mui/material";
import { Typography } from '@mui/material';
import React, { useState } from 'react';

interface props {
  directoryName: string
}

const DisplayImages = ({ directoryName }: props) => {
  const [availableImages, setAvailableImages] = useState<Array<string>>([]);
  const [selectedImages, setSelectedImages] = useState<Array<string>>([]);
  const [deltaError, setDeltaError] = useState<string>('');
  const [displayDeltaError, setDisplayDeltaError] = useState<boolean>(false);

  const getAvailableImages = () => {
    fetch("http://localhost:8000/images/list")
      .then((response) => response.json())
      .then((json) => {
        setAvailableImages(json.images)
      });
  };

  const initiateDelta = () => {
    console.log('Lenght: ', selectedImages.length);
    if (selectedImages.length < 2) {
      setDisplayDeltaError(true)
      setDeltaError('Unable to initiate delta - amount of selected images to low');
      // setDeltaError('Unable to initiate delta - amount of selected images to low');
      // const intervalId = setInterval(() => {
      //   console.log('Interval', displayDeltaError)
      //   if (displayDeltaError == 'visible') {
      //     console.log('Set to hidden')
      //     setDisplayDeltaError('hidden');
      //     setDeltaError('');
      //     clearInterval(intervalId);
      //   } else {
      //     console.log('Set to visible')
      //     setDisplayDeltaError('visible');
      //     setDeltaError('Unable to initiate delta - amount of selected images to low');
      //   }
      // }, 1500);
    }
    else {
      const data = { 'images': selectedImages }
      setDeltaError('');
      setDisplayDeltaError(false)

      fetch("http://localhost:8000/delta", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      }).then(async (e) => {
        let data = await e.json()
        console.log('Data: ', data)
        directoryName = data['directoryName']
      }).catch(e => console.log('Error', e))      
    }
  }

  const addImageForComparison = (e: any) => {
    const image = e.target.getAttribute('data-name');
    setSelectedImages((selectedImages) => {
      if (selectedImages.includes(image)) {
        const imagesArray = selectedImages.filter(name => 
          image !== name
        )
        return imagesArray
      }
      else {
        return [image, ...selectedImages]
      }
    })
  }


  return (
    <>
      <h2>Images</h2>
      <h3>Selected Images</h3>
      {/* <Typography variant="h3" sx={{ fontSize: 24, color: 'white', fontWeight: 'bold' }} >Selected Images</Typography> */}
      <Box sx={{ display: 'flex' }}>
        {selectedImages.map((name, index) => (
          <Box
            key={index}
            data-name={name}
            onClick={addImageForComparison}
            sx={{
              textAlign: "left",
              fontSize: 18,
              fontWeight: "bold",
              margin: '1rem',
              pading: '1.5rem',
              color: 'black',
              backgroundColor: 'white',
              cursor: 'pointer',
              width: 'auto'
            }}
          >
            {name}
          </Box>
        ))}
      </Box>
      <h3>Available Images</h3>
      <div>
        {availableImages.map((name, index) => (
          <Box
            key={index}
            data-name={name}
            onClick={addImageForComparison}
            sx={{
              textAlign: "left",
              fontSize: 24,
              fontWeight: "bold",
              color: "white",
              margin: '1rem',
              padding: '0.5rem',
              border: '1px solid white',
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            {name}
          </Box>
        ))}
      </div>
      <Button variant="contained" sx={{ marginTop: '1rem' }} onClick={getAvailableImages}>
        Retrieve Images
      </Button>
      <Button variant="contained" sx={{ marginTop: '1rem' }}  onClick={initiateDelta}>
        Initiate Delta
      </Button>
      {
        displayDeltaError ?
          <Alert sx={{ marginTop: '1rem' }} severity="error">{deltaError}</Alert>
        : ''
      }
    </>
  );
}

export default DisplayImages;
