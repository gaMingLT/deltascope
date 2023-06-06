
# Deltascope

This repo is made for my Bachelor Thesis of 2023 at Howest Bruges. The application performs Delta Baselining when two raw disk images (states) are entered as input.

More information can be found in the accompanying thesis explaining ``Delta Baselining: File System`` concept & the application [here - ADD LINK]().

## Description

The application uses the ``fls``, ``mactime`` and ``grep`` utilities under the hood to perform Delta Baselining on the file system when two states (raw disk images) are provided as input.

## Architecture

The application consists of three components: api ``fastapi``, web ``NextJS``, cli ``python``.

## Running the application

The API can be run by executing the ``uvicorn main:app --reload`` command, the web can be run by executing ``npm run dev``. All other required packages both for the api, cli & web need to be installed to be able to run the applications.
