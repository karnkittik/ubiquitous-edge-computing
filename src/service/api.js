import axios from "axios";
import config from "../configs/config";

const edgeApi = axios.create({
  baseURL: `${config.edge_url}/`,
  headers: {
    "Content-Type": "application/json",
  },
});
const cloudApi = axios.create({
  baseURL: `${config.cloud_url}/`,
  headers: {
    "Content-Type": "application/json",
  },
});

edgeApi.interceptors.request.use((x) => {
  x.meta = x.meta || {};
  x.meta.requestStartedAt = new Date().getTime();
  return x;
});

edgeApi.interceptors.response.use(
  (x) => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
  },
  (err) => {
    throw err;
  }
);

cloudApi.interceptors.request.use((x) => {
  x.meta = x.meta || {};
  x.meta.requestStartedAt = new Date().getTime();
  return x;
});
cloudApi.interceptors.response.use(
  (x) => {
    x.responseTime = new Date().getTime() - x.config.meta.requestStartedAt;
    return x;
  },
  (err) => {
    throw err;
  }
);
const queryService = {
  edgePeopleCounting(img, modelSize) {
    // MockTest;
    return new Promise((resolve, reject) => {
      setTimeout(
        () =>
          resolve({
            data: { building: "A", floor: "1", tag: "21" },
            responseTime: 235.5,
          }),
        1000
      );
    });
    return cloudApi.post("/get-location", {
      building_id: fps[qId - 1].b_id,
      finger_print: fps[qId - 1].fp,
    });
    return new Promise((resolve, reject) => {
      reject(new Error("wrong arguement"));
    });
  },
  cloudPeopleCounting(img, modelSize) {
    // MockTest;
    return new Promise((resolve, reject) => {
      setTimeout(
        () =>
          resolve({
            data: { building: "A", floor: "1", tag: "21" },
            responseTime: 235.5,
          }),
        1000
      );
    });
  },
  //   indoorQuery(arch, qId) {
  //     // MockTest;
  //     // return new Promise((resolve, reject) => {
  //     //   setTimeout(
  //     //     () =>
  //     //       resolve({
  //     //         data: { building: "A", floor: "1", tag: "21" },
  //     //         responseTime: 235.5,
  //     //       }),
  //     //     1000
  //     //   );
  //     // });
  //     if (arch === "A") {
  //       return cloudApi.post("/get-location", {
  //         building_id: fps[qId - 1].b_id,
  //         finger_print: fps[qId - 1].fp,
  //       });
  //     }
  //     if (arch === "B") {
  //       return edgeApi.post("/get-location", {
  //         building_id: fps[qId - 1].b_id,
  //         finger_print: fps[qId - 1].fp,
  //       });
  //     }
  //     return new Promise((resolve, reject) => {
  //       reject(new Error("wrong arguement"));
  //     });
  //   },
};
export default queryService;
