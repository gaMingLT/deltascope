import { Box, Button } from "@mui/material";
import { Typography } from '@mui/material';
import React, { useState, useEffect } from 'react';


const DisplayImages = () => {
  const [availableImages, setAvailableImages] = useState<Array<string>>([]);
  const [selectedImages, setSelectedImages] = useState<Array<string>>([]);

  const getAvailableImages = () => {
    fetch("http://localhost:8000/images/list")
      .then((response) => response.json())
      .then((json) => {
        setAvailableImages(json.images)
      });
  };

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
      <div>
        {selectedImages.map((name, index) => (
          <Box
            key={index}
            data-name={name}
            onClick={addImageForComparison}
            sx={{
              textAlign: "left",
              fontSize: 16,
              fontWeight: "",
              color: "white",
              margin: '1rem'
            }}
          >
            {name}
          </Box>
        ))}
      </div>
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
              margin: '1rem'
            }}
          >
            {name}
          </Box>
        ))}
      </div>
      <Button variant="contained" onClick={getAvailableImages}>
        Retrieve Images
      </Button>
    </>
  );
}

export default DisplayImages;
