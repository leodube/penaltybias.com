import axios from "axios";

export default {
  get: async () => {
    let res = await axios.get(
      "http://localhost:5000/api/predict-penalties"
    );
    return res.data || [];
  },
};
