import { DataGrid, GridRowsProp, GridColDef } from "@mui/x-data-grid";
import {
  Alert,
  AppBar,
  Box,
  Button,
  Grid,
  Tab,
  Tabs,
  Typography,
} from "@mui/material";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { useEffect, useState } from "react";

const columns: GridColDef[] = [
  {
    field: "date",
    headerName: "Date",
    width: 250,
  },
  { field: "size", headerName: "Size", width: 100 },
  { field: "activity", headerName: "Acitvity", width: 125 },
  { field: "permissions", headerName: "Permissions", width: 125 },
  { field: "uid", headerName: "User ID", width: 100 },
  { field: "guid", headerName: "Group ID", width: 100 },
  { field: "inode", headerName: "Inode", width: 75 },
  { field: "name", headerName: "Name", width: 250 },
];

const DisplayEvents = ({
  images,
  directoryName,
  setEventsParent
}: {
  images: Array<string>;
  directoryName: string;
  setEventsParent: any;
}) => {
  const [value, setValue] = useState(0);
  const [events, setEvents] = useState({
    delta: new Array(),
    base: new Array(),
    next: new Array(),
  });
  // const [eventsSet, setEventsSet] = useState<boolean>(false);
  const [ErrorMessage, setDeltaError] = useState<string>("");
  const [displayError, setDisplayErrorMessage] = useState<boolean>(false);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  // useEffect(() => {
  //   if(eventsSet) {
  //     eventsToTable(events)
  //   }
  // })

  const eventsToTable = (events: any) => {
    console.log('Events to table!', events)
    const tempEventsData = {
      delta: new Array(),
      base: new Array(),
      next: new Array(),
    };

    
    Object.keys(events).map((key: string) => {

        const eventsType = events[key]
        let idCounter = 0;
        let previousDate = "";
        eventsType.forEach((element: any) => {
          
          let itemToAdd: any = {
            id: idCounter, 
            date: element[0] ? element[0] : previousDate,
            size: element[1],
            activity: element[2],
            permissions: element[3],
            uid: element[4],
            guid: element[5],
            inode: element[6],
            name: element[7]
          }

          element[0] ? previousDate = element[0] : ""

          switch(key) {
            case "delta":
              tempEventsData.delta.push(itemToAdd);
              break;
            case "next":
              tempEventsData.next.push(itemToAdd);
              break;
            case "base":
              tempEventsData.base.push(itemToAdd);
              break;
            default:
              break;
          }
          
          idCounter++;
        })

        // setEventsSet(true)
    })

    console.log("Events data - mapped: ", tempEventsData)
    setEvents(tempEventsData)

    console.log("Events: ", events.delta)
    
  }

  const getEvents = () => {
    const data = { directoryName: directoryName, images: images };

    fetch("http://localhost:8000/events/", {
      method: "POST",
      body: JSON.stringify(data),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then(async (e) => {
        let data = await e.json();
        setEventsParent(data)
        eventsToTable(data.events);
      })
      .catch((e) => {
        setDisplayErrorMessage(true);
        setDeltaError("Unable to retrieve events");
      });
  };

  return (
    <>
      <Grid container spacing="2">
        <Grid item>
        <TabContext value={value.toString()}>
                <Box sx={{ borderBottom: 1, borderColor: "divider" }}>
                  <TabList
                    onChange={handleChange}
                    aria-label="lab API tabs example"
                  >
                    <Tab label="Delta's" value="0" />
                    <Tab label="Base Image" value="1" />
                    <Tab label="Next Image" value="2" />
                  </TabList>
                </Box>

                <TabPanel value="0">
                  <Box height={'350px'} width='100%'>
                    <DataGrid
                      sx={{ fontSize: "1.2rem" }}
                      rows={events.delta}
                      columns={columns}
                    />                    
                  </Box>
                </TabPanel>

                <TabPanel value="1">
                  <Box height={'350px'}  width='100%'>
                    <DataGrid
                        sx={{ fontSize: "1.2rem" }}
                        rows={events.base}
                        columns={columns}
                      />                    
                  </Box>
                </TabPanel>

                <TabPanel value="2">
                  <Box height={'350px'}  width='100%'>
                    <DataGrid
                        sx={{ fontSize: "1.2rem" }}
                        rows={events.next}
                        columns={columns}
                      />                    
                  </Box>
                </TabPanel>

              </TabContext>
        </Grid>
        <Grid item container spacing="2" direction="column">
          <Grid item>
            <Box>
              <Button variant="contained" sx={{ margin: "1rem" }} onClick={getEvents}>
                Get Events
              </Button>                
            </Box>
          </Grid>
          <Grid item>
            <Box>
              {displayError ? (
                <Alert sx={{ marginTop: "1rem" }} severity="error">
                  {ErrorMessage}
                </Alert>
              ) : (
                ""
              )}
            </Box>
          </Grid>
        </Grid>       
      </Grid>
    </>
  );
};

export default DisplayEvents;
