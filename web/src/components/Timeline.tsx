import { Box, Grid } from "@mui/material";
import { useEffect, useState } from "react";
import { Timeline } from "vis-timeline";
// import "vis-timeline/styles/vis-timeline-graph2d.css";

const DisplayTimeline = ({ eventsData }: { eventsData: any }) => {
  const [timeLineLoaded, setTimeLineLoaded] = useState<Boolean>(false)
  const [selectedEventsTimeline, setSelectedEventsTimeline] = useState<{ modified: boolean, accessed: boolean, changed: boolean, created: boolean }>(
    {
      "modified": true,
      "accessed": true,
      "changed": true,
      "created": true
    }
  );

  useEffect(() => { 
    if (!timeLineLoaded && eventsData) {
      createTimeline()
      setTimeLineLoaded(true)
    }
  })

  const changeEventsShown = (type: string) => {
    switch(type) {
      case "modified":
        selectedEventsTimeline.modified = !selectedEventsTimeline.modified;
        break;
      case "accessed":
        selectedEventsTimeline.accessed = !selectedEventsTimeline.accessed;
        break;
      case "changed":
        selectedEventsTimeline.changed = !selectedEventsTimeline.changed;
        break;
      case "created":
        selectedEventsTimeline.created = !selectedEventsTimeline.created;
        break;
    }
    createTimeline();
  }

  const addToTimeline = (element: string) => {
    let res = false
    Object.keys(selectedEventsTimeline).map((key: string) => {
      const temp= selectedEventsTimeline as any;
      if (element == key) {
        res = temp[key]
      } 
    })
    return res;
  }

  const createTimeline = () => {
    const container = document.getElementById("visualization") as HTMLElement;
    container.innerHTML = "";

    const groups = [
      { content: "Delta", id: "delta", value: 1, className: "delta" },
    ]

    const items: Array<any> = []
    let idCounter = 0;
    const events = eventsData["events"]
    const deltaEvents = events.delta
    deltaEvents.map((element: any) => {
      const path = element.Path
      const name = path.split('/')[-1]
      let fileType;

      switch(element.FileType[0]) {
        case "-":
          fileType = "Unknown"
          break;
        case "r":
          fileType = "Regular File"
          break;
        case "d":
          fileType = "Directory"
          break;
        case "l":
          fileType = "Link"
          break;
        default:
          fileType = element.FileType[0]
          break;
      }

      const divContent = `      
        <div style={{ width: '25px', height: '25px', padding: '0.5rem', wordWrap: 'break-word' }} >
          <p>Path: ${path}</p>
          <p>Type: ${fileType}</p>
         </div>`

      let itemToAdd: any = { id: idCounter, content: divContent , start: element.Date }

      if (element.bActivity != ".") {
        itemToAdd.className = "created"
      }
      else if (element.mActivity != ".")  {
        itemToAdd.className = "modified"
      }      
      else if (element.aActivity != ".") {
        itemToAdd.className = "accessed"
      }
      else if (element.cActivity != ".") {
        itemToAdd.className = "changed"
      }


      if (addToTimeline(itemToAdd.className)) {
        items.push(itemToAdd);
        idCounter++;
      }

    })

    // Configuration for the Timeline
    const options = {
      height: '450px',
      stack: true,
      horizontalScroll: true,
      // verticalScroll: true, 
      // zoomKey: 'ctrlKey'
    }

    // Create a Timeline
    const timeline = new Timeline(container, items, options);
  }


  return (
    <>
      <Grid container spacing={4} direction="column">
        {/* <Grid item>
          <Box style={{ textAlign: 'center', width: '100%', margin: 'auto' }} >
            <h1>Pipeline</h1>
          </Box>
        </Grid> */}
        <Grid item>
          <Box id="visualization" style={{ border: '1px solid black', height: '475px', margin: '1rem', padding: '0.5rem', backgroundColor: "white" }}>
          </Box>
        </Grid>
        <Grid item container spacing={2} justifyContent={"center"} p={1} width={"max-content"} margin={"auto"} /* style={{ backgroundColor: '#42a5f5' }} */ >
            <Grid item>
              <Box style={{ display: 'flex' ,justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', padding: '0.25rem', borderRadius: '5px', cursor: 'pointer'  }} onClick={() => changeEventsShown("modified")} >
                <h3>Modified: </h3>
                <div style={{ height: '2rem', width: '2rem', backgroundColor: 'rgb(31, 201, 53)', margin: '0.5rem' , borderRadius: '5px' }} ></div>
              </Box>
            </Grid>
            <Grid item>
            <Box style={{ display: 'flex' ,justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', padding: '0.25rem', borderRadius: '5px', cursor: 'pointer'  }} onClick={() => changeEventsShown("accessed")} >
                <h3>Accessed: </h3>
                <div style={{ height: '2rem', width: '2rem', backgroundColor: 'rgb(95, 91, 91)', margin: '0.5rem' ,borderRadius: '5px' }} ></div>
              </Box>
            </Grid>
            <Grid item>
              <Box style={{ display: 'flex' ,justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', padding: '0.25rem', borderRadius: '5px', cursor: 'pointer'  }} onClick={() => changeEventsShown("changed")} >
                <h3>Changed: </h3>
                <div style={{ height: '2rem', width: '2rem', backgroundColor: 'rgb(229, 108, 108)', margin: '0.5rem' ,borderRadius: '5px' }} ></div>
              </Box>
            </Grid>
            <Grid item>
              <Box style={{ display: 'flex' ,justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'white', padding: '0.25rem', borderRadius: '5px', cursor: 'pointer'  }} onClick={() => changeEventsShown("created")}  >
                <h3>Created: </h3>
                <div style={{ height: '2rem', width: '2rem', backgroundColor: 'aqua', margin: '0.5rem' ,borderRadius: '5px' }} ></div>
              </Box>
            </Grid>
        </Grid>
      </Grid>
    </>
  )
}

export default DisplayTimeline;
