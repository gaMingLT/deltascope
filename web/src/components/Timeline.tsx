import { Box, Grid } from "@mui/material";
import { useEffect, useState } from "react";
import { Timeline } from "vis-timeline";
// import "vis-timeline/styles/vis-timeline-graph2d.css";


const DisplayTimeline = ({ eventsData }: { eventsData: any }) => {
  const [timeLineLoaded, setTimeLineLoaded] = useState<Boolean>(false)

  useEffect(() => { 
    if (!timeLineLoaded && eventsData) {
      createTimeline()
      setTimeLineLoaded(true)
    }
  })

  const createTimeline = () => {
    const container = document.getElementById("visualization") as HTMLElement;
    container.innerHTML = "";

    const groups = [
      { content: "Base", id: "base", value: 1, className: "base" },
      // { content: "Next", id: "next", value: 2, className: "next" },
      { content: "Delta", id: "delta", value: 3, className: "delta" },
    ]

    const items: Array<any> = []
    let idCounter = 0;
    const events = eventsData["events"]
    Object.keys(events).map((key: string) => {

      if (key != "next") {
        const eventsType = events[key]

        eventsType.forEach((element: any) => {
          let itemToAdd: any = { id: idCounter, content: `${element[7]} \n ${element[2]}` ,start: element[0] }
          
          if (key == "base") {
              itemToAdd.group = "base";
              itemToAdd.className = "base";
          }

          // if (key == "next") {
          //   itemToAdd.group = "next";
          //   itemToAdd.className = "next";
          // }

          if (key == "delta") {
            itemToAdd.group = "delta";
            itemToAdd.className = "delta";
          }

          items.push(itemToAdd);

          idCounter++;
        });        
      }
    })

    // Configuration for the Timeline
    const options = {
      // height: '300px'
    }

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
