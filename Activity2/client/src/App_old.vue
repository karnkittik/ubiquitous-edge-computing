<template>
  <div class="main">
    <h1 class="RED-Taylor's-Version-is-out-12-November">
      Welcome to Edge-Cloud Architecture
    </h1>
    <table>
      <tbody>
        <tr>
          <th>Query ID</th>
          <th>Response <br />Architecture A: Central-Cloud Architecture</th>
          <th>
            Response <br />
            Architecture B: Edge-Cloud Architecture
          </th>
          <th>Query by Using</th>
        </tr>
        <tr v-for="(query, index) in queries" :key="query.qId">
          <td>{{ query.qId }}</td>
          <td v-if="query.loadingA">Loading..</td>
          <td v-else class="response">
            <div>
              <span class="title">Location: </span
              >{{
                query.responseA ? JSON.stringify(query.responseA.location) : ""
              }}
            </div>
            <div>
              <span class="title">Response time: </span>
              {{ query.responseA ? `${query.responseA.responseTime} ms` : "" }}
            </div>
          </td>
          <td v-if="query.loadingB">Loading..</td>
          <td v-else class="response">
            <div>
              <span class="title">Location: </span
              >{{
                query.responseB ? JSON.stringify(query.responseB.location) : ""
              }}
            </div>
            <div>
              <span class="title">Response time: </span>
              {{ query.responseB ? `${query.responseB.responseTime} ms` : "" }}
            </div>
          </td>
          <td>
            <div class="mode-selector">
              <button @click="queryArch('A', query.qId, index)">
                Architecture A
              </button>
              <button @click="queryArch('B', query.qId, index)">
                Architecture B
              </button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
<!-- <script>
import queryService from "./service/api";
export default {
  name: "Home",
  data() {
    return {
      // EditHere
      queries: [
        {
          qId: "1",
          loadingA: false,
          loadingB: false,
          responseA: null,
          responseB: null,
        },
      ],
    };
  },
  methods: {
    async queryArch(arch, qId, index) {
      this.queries[index][`loading${arch}`] = true;
      this.queries[index][`response${arch}`] = null;
      await queryService
        .indoorQuery(arch, qId)
        .then(({ data: location, responseTime }) => {
          const response = { location, responseTime };
          this.queries[index][`response${arch}`] = response;
        })
        .catch((err) => {
          console.log(err.message);
        });
      this.queries[index][`loading${arch}`] = false;
    },
  },
};
</script> -->

<style scoped>
.mode-selector {
  display: flex;
  column-gap: 30px;
  justify-content: center;
}
table {
  font-family: arial, sans-serif;
  border-collapse: collapse;
  width: 100%;
  margin: 20px 0;
}

td,
th {
  border: 1px solid #dddddd;
  text-align: left;
  padding: 8px;
  text-align: center;
}

tr:nth-child(even) {
  background-color: #f4f2f2;
}

button {
  min-height: 30px;
}
.title {
  color: #6e5aa5;
  font-weight: bolder;
  margin-right: 10px;
}
.response {
  text-align: left;
}
</style>
