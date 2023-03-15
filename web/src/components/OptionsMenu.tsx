import { AppBar, Box, Grid, Tab, Tabs, Typography } from "@mui/material";
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import { useState } from "react";
import DisplayEvents from "./DisplayEvents";
import DisplayFiles from "./DisplayFiles";


const ImageActions = ({ directory, images}: {directory: any, images: any}) => {
  const [value, setValue] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <>
      <Box sx={{ width: '100%' }}>
        <h1>Menu</h1>
        <Box sx={{ width: 'max-content', typography: 'body1' }}>
          <TabContext value={value.toString()} >
            <Box sx={{ borderBottom: 1, borderColor: 'divider', backgroundColor: 'lightblue' }}>
              <TabList onChange={handleChange} aria-label="lab API tabs example" variant="fullWidth">
                <Tab label="Events" value="0" />
                <Tab label="Files" value="1" />
              </TabList>
            </Box>
            <TabPanel value="0">
              <Grid container direction={"row"} spacing={4} item>
                <DisplayEvents images={images} directoryName={directory}  />
              </Grid>
            </TabPanel>
            <TabPanel value="1">
              <Grid container direction={"row"} spacing={4} item>
                <DisplayFiles />
              </Grid>
            </TabPanel>
          </TabContext>
        </Box>
      </Box>
    </>
  )
}

export default ImageActions;
