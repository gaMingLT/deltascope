import { AppBar, Box, Grid, Tab, Tabs, Typography } from "@mui/material";
import TabContext from '@mui/lab/TabContext';
import TabList from '@mui/lab/TabList';
import TabPanel from '@mui/lab/TabPanel';
import { useState } from "react";
import DisplayEvents from "./DisplayEvents";
import FileDisplay from "./File";


const ImageActions = () => {
  const [value, setValue] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <>
      <h1>Menu</h1>
      <Box sx={{ width: '100%', typography: 'body1' }}>
      <TabContext value={value.toString()}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider', backgroundColor: 'lightblue' }}>
          <TabList onChange={handleChange} aria-label="lab API tabs example">
            <Tab label="Events" value="0" />
            <Tab label="Files" value="1" />
          </TabList>
        </Box>
        <TabPanel value="0">
          <Grid container direction={"row"} spacing={2} item>
            <DisplayEvents />
          </Grid>
        </TabPanel>
        <TabPanel value="1">
          <Grid container direction={"row"} spacing={2} item>
            <FileDisplay />
            <FileDisplay />
          </Grid>
        </TabPanel>
      </TabContext>
    </Box>
    </>
  )
}

export default ImageActions;
