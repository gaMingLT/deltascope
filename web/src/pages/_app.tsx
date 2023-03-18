import { type AppType } from "next/dist/shared/lib/utils";
import "vis-timeline/styles/vis-timeline-graph2d.css";
import "~/styles/globals.css";

const MyApp: AppType = ({ Component, pageProps }) => {
  return <Component {...pageProps} />;
};

export default MyApp;
