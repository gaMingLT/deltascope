import { Alert, Box, Button } from "@mui/material";
import { Typography } from '@mui/material';
import React, { useState } from 'react';


const DisplayImages = ({ setParentDirectoryName, setImages }: { setParentDirectoryName: any, setImages: any }) => {
  const [availableImages, setAvailableImages] = useState<Array<string>>([]);
  const [selectedImages, setSelectedImages] = useState<Array<string>>([]);
  const [ErrorMessage, setDeltaError] = useState<string>('');
  const [displayError, setDisplayErrorMessage] = useState<boolean>(false);
  const [ message, setMessage ] = useState<string>('');
  const [displayMessage, setDisplayMessage] = useState<boolean>(false);

  const getAvailableImages = () => {
    console.log('Fetching available images')
    fetch("http://localhost:8000/images/list")
      .then((response) => response.json())
      .then((json) => {
        setAvailableImages(json.images)
      }).catch((e) => {
        setDisplayErrorMessage(true)
        setDeltaError('Unable to retrieve available images for comparison');
      });
  };

  const initiateDelta = () => {
    if (selectedImages.length < 2) {
      setDisplayErrorMessage(true)
      setDeltaError('Unable to initiate delta - amount of selected images to low');
      setTimeout(() => setDisplayErrorMessage(false),2000);
    }
    else {
      const data = { 'images': selectedImages, 'directoryNames': '' }
      setDeltaError('');
      setDisplayErrorMessage(false)

      fetch("http://localhost:8000/delta", {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
          "Content-Type": "application/json",
        },
      }).then(async (e) => {
        let data = await e.json()
        console.log('Data: ', data)
        setParentDirectoryName(data['directoryName'])
        setImages(data['images'])
        setMessage('Deltaing images - succesfull!')
        setDisplayMessage(true)
        setTimeout(() => setDisplayMessage(false),2000);

      }).catch((e) =>  {
        setDisplayErrorMessage(true)
        setDeltaError('Unable to initiate delta beteween selected images');
        setTimeout(() => setDisplayErrorMessage(false),2000);
      })      
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
    <Box sx={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-around', padding: '1rem', margin: '1rem', border: '1px solid white', borderRadius: '5px' }} >
    <Typography variant="h2" sx={{ fontSize: '2.25rem', fontWeight: 'bolder' }} >Images</Typography>
      <Typography variant="h5" sx={{ fontSize: '1.5rem', fontWeight: 'bolder' }} >Selected Images</Typography>
      {/* <Typography variant="h3" sx={{ fontSize: 24, color: 'white', fontWeight: 'bold' }} >Selected Images</Typography> */}
      <Box sx={{ display: 'flex', flexWrap: 'wrap', border: '1px solid white', minWidth: 'max', minHeight: '10%' }}>
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
              pading: '1rem',
              color: 'black',
              backgroundColor: 'lightblue',
              cursor: 'pointer',
              width: 'auto',
              borderRadius: '5px'
            }}
          >
            {name}
          </Box>
        ))}
      </Box>
      <Typography variant="h5" sx={{ fontSize: '1.5rem', fontWeight: 'bolder' }} >Available Images</Typography>
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
              color: "black",
              margin: '1rem',
              padding: '0.5rem',
              border: '2px solid black',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            {name}
          </Box>
        ))}
      </div>
      <Box sx={{ display: 'flex', flexDirection: 'column' }} >
        <Button variant="contained" sx={{ marginTop: '1rem' }} onClick={getAvailableImages}>
          Retrieve Images
        </Button>
        <Button variant="contained" sx={{ marginTop: '1rem' }}  onClick={initiateDelta}>
          Initiate Delta
        </Button>
        {
          displayError ?
            <Alert sx={{ marginTop: '1rem' }} severity="error">{ErrorMessage}</Alert>
          : ''
        }
        {
          displayMessage ?
          <Alert sx={{ marginTop: '1rem' }} severity="success">{message}</Alert>
          : ''
        }  
      </Box>
      </Box>
    </>
  );
}

export default DisplayImages;
