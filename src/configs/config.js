const config = {
  edge_url: process.env.VUE_APP_EDGE_URL || "",
  cloud_url: process.env.VUE_APP_CLOUD_URL || "",
};

console.log("===========");
console.log(config.edge_url);
console.log(config.cloud_url);
console.log("===========");

export default config;
