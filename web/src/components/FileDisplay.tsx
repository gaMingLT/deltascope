import { Box, Button, Grid, TextareaAutosize, Typography } from "@mui/material";
import Textarea from '@mui/joy/Textarea';
import { useEffect, useRef, useState } from "react";
import  Editor, { useMonaco } from "@monaco-editor/react";

const FileDisplay = ({ fileBlob }: { fileBlob: Blob | undefined }) => {
  const [fileContent, setFileContent] = useState<string | ArrayBuffer | null>(
    ""
  );
  const [fileSet, setFileSet] = useState<boolean>(false);
  const monaco = useMonaco();

  useEffect(() => {
    if (fileBlob) {
      loadFile()
      setFileSet(true)
    }

  })

  const setEditorContent = (content: string) => {
    monaco?.editor.getModels()[0]?.setValue(content);
  } 

  const loadFile = () => {
    const reader = new FileReader();

    reader.addEventListener(
      "load",
      () => {
        setFileContent(reader.result);
        setEditorContent(reader.result as string);
      },
      false
    );

    if (fileBlob) {
      reader.readAsText(fileBlob);
    }
  };

  return (
    <>
      {/* <div className="flex flex-row justify-between items-center px-2 py-2 gap-5 w-full"> */}
      <div className="px-2 py-2" >
        <Editor
                  height="30vh"
                  theme="vs-light"
                  defaultLanguage="text"
                  defaultValue={"File Content Here!"}
              />
                 {/* <Button className="bg-slate-500 h-max" variant="contained" onClick={loadFile} >Load file</Button>  */}
      </div>

      {/* <Grid item container spacing={4} direction="column"> */}
        {/* <Grid item> */}
          {/* <Box> */}
            {/* <Typography variant="h5" >File Name here</Typography> */}
          {/* </Box> */}
        {/* </Grid> */}
        {/* <Grid item container spacing={2} direction="row"> */}
          {/* <Box padding={0.5} > */}
                 {/* <Editor
                  height="30vh"
                  theme="vs-light"
                  defaultLanguage="text"
                  defaultValue={"File Content Here!"}

                /> */}
          {/* </Box> */}
          {/* <Button className="bg-slate-500" variant="contained" onClick={loadFile} >Load file</Button>  */}
        {/* </Grid> */}
        {/* <Grid item>
            <Button variant="contained" onClick={loadFile} >Load file</Button>
        </Grid> */}
      {/* </Grid> */}
    </>
  );
};

export default FileDisplay;
