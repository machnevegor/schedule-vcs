const { ApolloServer } = require("apollo-server");
const { ApolloGateway } = require("@apollo/gateway");

const gateway = new ApolloGateway({
  serviceList: [{ name: "Schedule VCS", url: "http://localhost:8080" }],
});

const formatError = (error) => {
  return {
    serviceName: error.extensions.serviceName,
    message: error.extensions.exception.message,
    path: error.extensions.exception.path,
  };
};

const server = new ApolloServer({ gateway, formatError });

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
