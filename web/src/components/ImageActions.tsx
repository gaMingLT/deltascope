import { AppBar, Box, Grid, Tab, Tabs, Typography } from "@mui/material";
import TabContext from "@mui/lab/TabContext";
import TabList from "@mui/lab/TabList";
import TabPanel from "@mui/lab/TabPanel";
import { useState } from "react";
import DisplayEvents from "./DisplayEvents";
import DisplayFiles from "./DisplayFiles";

const ImageActions = ({
  directory,
  images,
}: {
  directory: any;
  images: any;
}) => {
  const [value, setValue] = useState(0);

  const handleChange = (event: React.SyntheticEvent, newValue: number) => {
    setValue(newValue);
  };

  return (
    <>
      <Grid
        container
        spacing={4}
        xs={8}
        direction={"column"}
        justifyContent="center"
        alignItems="center"
        zeroMinWidth
      >
        <Grid item>
          <Typography
            variant="h5"
            sx={{
              fontSize: "1.5rem",
              fontWeight: "bolder",
              textAlign: "center",
            }}
          >
            Menu
          </Typography>
        </Grid>

        <Grid
          container
          spacing={4}
          xs={8}
          item
          direction="row"
        >
          <TabContext value={value.toString()}>
            <Grid
              item
              xs
              sx={{
                borderBottom: 1,
                borderColor: "divider",
                backgroundColor: "lightblue",
              }}
            >
              <TabList
                onChange={handleChange}
                aria-label="lab API tabs example"
                variant="fullWidth"
              >
                <Tab label="Events" value="0" />
                <Tab label="Files" value="1" />
              </TabList>
            </Grid>

            <TabPanel value="0">
              <DisplayEvents images={images} directoryName={directory} />
            </TabPanel>

            <TabPanel value="1">
              <DisplayFiles directoryName={directory}  />
            </TabPanel>
          </TabContext>
        </Grid>
      </Grid>
    </>
  );
};

export default ImageActions;
