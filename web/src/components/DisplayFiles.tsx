import { Box, Grid } from "@mui/material"
import FileDisplay from "./FileDisplay"


const DisplayFiles = () => { 
  return(
  <>
  <Box sx={{ width: '100%', display: 'flex', justifyContent: 'space-between' }} >
      <FileDisplay fileBlob={new Blob(['Hello from 1'])} />
      <FileDisplay fileBlob={new Blob(['Hello from 2'])} />   
  </Box>
  </>
  )
}

export default DisplayFiles
