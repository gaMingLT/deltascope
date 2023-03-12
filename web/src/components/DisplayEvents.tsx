import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { Alert, AppBar, Box, Button, Grid, Tab, Tabs, Typography } from "@mui/material";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { useState } from "react";


interface Events {
  'delta': Array<EventRowType>,
  'base': Array<EventRowType>,
  'next': Array<EventRowType>
}

interface EventRowType extends GridRowsProp {
  id: number,
  date: string,
  size: number,
  activity: string,
  permissions: string,
  uid: number,
  guid: number,
  inode: number,
  name: string
}

// const rows: GridRowsProp = [
//   {
//     id: 1,
//     date: "Sat Feb 25 2023 16:27:26",
//     size: 16384,
//     activity: "macb",
//     permissions: "d/drwx------",
//     uid: 0,
//     guid: 0,
//     inode: 11,
//     name: "/lost+found",
//   },
//   // Sat Feb 25 2023 16:27:26	16384	macb	d/drwx------	0	0	11	/lost+found
// ];

const columns: GridColDef[] = [
  {
    field: "date",
    headerName: "Date",
    width: 150,
  },
  { field: "size", headerName: "Size", width: 150 },
  { field: "activity", headerName: "Acitvity", width: 150 },
  { field: "permissions", headerName: "Permissions", width: 150 },
  { field: "uid", headerName: "User ID", width: 150 },
  { field: "guid", headerName: "Group ID", width: 150 },
  { field: "inode", headerName: "Inode", width: 150 },
  { field: "name", headerName: "Name", width: 150 },
];

const DisplayEvents = () => {
  const [value, setValue] = useState(0);
  const [events, setEvents] = useState<Events>({ 'delta': [], 'base': [], 'next': [] })
  const [ErrorMessage, setDeltaError] = useState<string>('');
  const [displayError, setDisplayErrorMessage] = useState<boolean>(false);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const getEvents = () => {
    const data = {
      images: ["exp-changed.img", "another-change.img"],
      directoryName: "./output/deltascope-2023-03-12_20:25:28-918008",
    };
    console.log("Fetching!")
    fetch("http://localhost:8000/events/", {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    }).then(async (e) => {
      let data = await e.json()
      setEvents(data)
      console.log('Data: ', data)
    }).catch((e) =>  {
      setDisplayErrorMessage(true)
      setDeltaError('Unable to retrieve events');
    }) 
  }

  return (
    <>
    <Box style={{ display: 'flex', flexDirection: 'column'  }} >
      {/* <h1>Events</h1> */}
      <div>
        <p>Legend</p>
        {/* Differentiate in different images based on color */}
          <Button variant="contained" sx={{ margin: '1rem' }}  onClick={getEvents}>
            Get Events
          </Button>
      </div>
      <Box sx={{ width: "100%", typography: "body1" }}>
        <TabContext value={value.toString()}>
          <Box
            sx={{
              borderBottom: 1,
              borderColor: "divider",
              backgroundColor: "lightblue",
            }}
          >
            <TabList onChange={handleChange} aria-label="Events Menu">
              <Tab label="Delta's" value="0" />
              <Tab label="Base Image" value="1" />
              <Tab label="New Image" value="2" />
            </TabList>
          </Box>
          <TabPanel value="0">
            {/* FIXME: Data not being show on the page */}
            <DataGrid rows={events.delta} columns={columns} />
          </TabPanel>
          <TabPanel value="1">
            {/* <DataGrid rows={rows} columns={columns} /> */}
          </TabPanel>
          <TabPanel value="2">
            {/* <DataGrid rows={rows} columns={columns} /> */}
          </TabPanel>
        </TabContext>
          {
            displayError ?
              <Alert sx={{ marginTop: '1rem' }} severity="error">{ErrorMessage}</Alert>
            : ''
          }
      </Box>      
    </Box>

    </>
  );
};

export default DisplayEvents;
