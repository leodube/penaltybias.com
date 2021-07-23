import axios from "axios";

export default {
  get: async () => {
    let res = await axios.get(
      "https://penalty-bias.herokuapp.com/api/predict-penalties"
    );
    return res.data || [];
  },
};
