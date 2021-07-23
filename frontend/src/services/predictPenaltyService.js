import axios from "axios";

export default {
  get: async () => {
    let res = await axios.get(
      // "https://penalty-bias.herokuapp.com/api/predict-penalties"
      "http://127.0.0.1:5000/api/predict-penalties"
    );
    return res.data || [];
  },
};
