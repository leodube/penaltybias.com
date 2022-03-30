import axios from "axios";

export default {
  get: async () => {
    let res = await axios.get(
      "https://penaltybias-api.vercel.app/api/predict-penalties"
    );
    return res.data || [];
  },
};
