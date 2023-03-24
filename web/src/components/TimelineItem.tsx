import { Box, Grid } from "@mui/material";


const TimelineItem = ({ event }: { event: any }) => {
  return (
    <>
      <Box style={{ width: '25px', height: '25px', padding: '0.5rem', wordWrap: 'break-word' }} >
        {/* <p>Path: {name}</p> */}
        {/* <p>Type: {fileType}</p> */}
      </Box>
    </>
  )
}

export default TimelineItem;
