import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import { Alert, AppBar, Box, Button, Grid, Tab, Tabs, Typography } from "@mui/material";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { useState } from "react";


const rowsDelta: GridRowsProp   = [
  {
    id: 1,
    date: "Sat Feb 25 2023 16:27:26",
    size: 16384,
    activity: "macb",
    permissions: "d/drwx------",
    uid: 0,
    guid: 0,
    inode: 11,
    name: "/lost+found",
  },
];

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

const rowsTest: GridRowsProp = [
  { id: 1, col1: 'Hello', col2: 'World' },
  { id: 2, col1: 'DataGridPro', col2: 'is Awesome' },
  { id: 3, col1: 'MUI', col2: 'is Amazing' },
];

const columnsTest: GridColDef[] = [
  { field: 'col1', headerName: 'Column 1', width: 150 },
  { field: 'col2', headerName: 'Column 2', width: 150 },
];

const DisplayEvents = ({ images, directoryName }: { images: Array<string>, directoryName: string }) => {
  const [value, setValue] = useState(0);
  const [events, setEvents] = useState({
    'delta': [], 'base': [], 'next': []
  })
  const [ErrorMessage, setDeltaError] = useState<string>('');
  const [displayError, setDisplayErrorMessage] = useState<boolean>(false);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  const getEvents = () => {
    console.log("Fetching!")
    const data = { 'directoryName': directoryName, 'images': images }
    console.log('Data - input: ', data)

    fetch("http://localhost:8000/events/", {
      method: 'POST',
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    }).then(async (e) => {
      let data = await e.json()
      console.log('Data: ', data)
    }).catch((e) =>  {
      setDisplayErrorMessage(true)
      setDeltaError('Unable to retrieve events');
    }) 
  }

  return (
    <>
    <Box style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center'  }} >
      <Box sx={{ width: "100%", typography: "body1", marginTop: '2rem' }}>
        <TabContext value={value.toString()}>
          <Box
            sx={{
              borderBottom: 1,
              borderColor: "divider",
              backgroundColor: "lightblue",
            }}
          >
            <TabList onChange={handleChange} aria-label="Events Menu" variant="fullWidth" centered>
              <Tab label="Delta's" value="0" />
              <Tab label="Base Image" value="1" />
              <Tab label="New Image" value="2" />
            </TabList>
          </Box>
          <TabPanel value="0">
            {/* FIXME: Data not being show on the page */}
            <DataGrid sx={{ color: 'white', fontSize: '1.2rem' }} rows={events.delta} columns={columns} />
          </TabPanel>
          <TabPanel value="1">
            <DataGrid sx={{ color: 'white', fontSize: '1.2rem' }} rows={events.base} columns={columns} />
          </TabPanel>
          <TabPanel value="2">
            <DataGrid sx={{ color: 'white', fontSize: '1.2rem' }} rows={events.next} columns={columns} />
          </TabPanel>
        </TabContext>
          {
            displayError ?
              <Alert sx={{ marginTop: '1rem' }} severity="error">{ErrorMessage}</Alert>
            : ''
          }
      </Box>
      <Button variant="contained" sx={{ margin: '1rem' }}  onClick={getEvents}>
            Get Events
          </Button>
    </Box>

    </>
  );
};

export default DisplayEvents;
