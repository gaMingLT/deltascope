import { Box, Grid } from "@mui/material";
import { useEffect, useState } from "react";
import { Timeline } from "vis-timeline";
// import "vis-timeline/styles/vis-timeline-graph2d.css";


const DisplayTimeline = () => {
  const [timeLineLoaded, setTimeLineLoaded] = useState<Boolean>(false)

  useEffect(() => { 
    if (!timeLineLoaded) {
      createTimeline()
    }
  })

  const createTimeline = () => {
    console.log('Clicking - timeline!')
    const container = document.getElementById("visualization") as HTMLElement;
    container.innerHTML = "";

    const groups = [
      { content: "Base", id: "base", value: 1, className: "base" },
      { content: "Next", id: "next", value: 2, className: "next" },
      { content: "Delta", id: "delta", value: 3, className: "delta" },
    ]

    // Create a DataSet (allows two way data-binding)
    const items = [
      {
        id: 1, content: "Base - item 1", start: "Sat Feb 25 2023 16:27:26", group: "base",
        className: "base"
      },
      { id: 2, content: "Base - item 2", start: "Sat Feb 25 2023 16:28:49", group: "base",
      className: "base" },
      { id: 3, content: "Base - item 3", start: "Sat Feb 25 2023 16:29:30", group: "base",
      className: "base" },

      {
        id: 4, content: "Next - item 1", start: "Sat Feb 25 2023 16:27:26", group: "next",
        className: "next"
      },
      { id: 5, content: "Next - item 2", start: "Sat Feb 25 2023 16:28:49", group: "next",
      className: "next" },
      { id: 6, content: "Next - item 3", start: "Sat Feb 25 2023 16:29:30", group: "next",
      className: "next" },

      {
        id: 7, content: "Delta - item 1", start: "Sat Feb 25 2023 16:27:26", group: "delta",
        className: "delta"
      },
      { id: 8, content: "Delta - item 2", start: "Sat Feb 25 2023 16:28:49", group: "delta",
      className: "delta" },
      { id: 9, content: "Delta - item 3", start: "Sat Feb 25 2023 16:29:30", group: "delta",
      className: "delta" },

    ];

    // Configuration for the Timeline
    const options = {
      min: "Sat Feb 25 2023 16:25:00", // lower limit of visible range
      max: "Sat Feb 25 2023 16:30:00",
    };

    // Create a Timeline
    const timeline = new Timeline(container, items, groups ,options);
  }


  return (
    <>
      <Grid container spacing={2} direction="column">
        <Grid item>
          <Box style={{ textAlign: 'center', width: '100%', margin: 'auto' }} >
            <h1>Pipeline</h1>
          </Box>
        </Grid>
        <Grid item>
          <Box id="visualization" style={{ border: '1px solid black', height: 'auto', margin: '1rem', padding: '1rem' }}>
          </Box>
        </Grid>
      </Grid>
    </>
  )
}

export default DisplayTimeline;
