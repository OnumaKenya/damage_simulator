import streamlit as st
import pandas as pd
from streamlit.column_config import NumberColumn, SelectboxColumn, TextColumn
from damage_simulator.buffs import Buff, Debuff
from damage_simulator.constants import BUFF_DIR, DEBUFF_DIR


def buff_df_input():
    with st.expander("バフ入力", expanded=True):
        column_config = {
            "バフ種": SelectboxColumn(
                options=list(map(lambda x: x.value, Buff.__members__.values())),
                width=200,
                required=True,
            ),
            "バフ量": NumberColumn(required=True),
            "備考": TextColumn(width=200),
        }
        if "buff" not in st.session_state:
            data = {
                "バフ種": [],
                "バフ量": [],
                "備考": [],
            }
            buff_list_df = pd.DataFrame(data).astype(
                {"バフ種": "str", "バフ量": "float", "備考": "str"}
            )
        else:
            buff_list_df = st.session_state.buff
        buff_list_df = st.data_editor(
            buff_list_df, column_config=column_config, num_rows="dynamic"
        )
        buff_list_df = buff_list_df[["バフ種", "バフ量", "備考"]].reset_index(drop=True)

    with st.expander("バフプリセット保存・読み込み", expanded=False):
        buff_preset_name = st.text_input("バフプリセット名")
        if st.button("バフ保存"):
            if (BUFF_DIR / f"{buff_preset_name}.csv").exists():
                buff_list_df.to_csv(BUFF_DIR / f"{buff_preset_name}.csv", index=False)
                st.warning("同名のバフプリセットを上書きしました。")
            else:
                buff_list_df.to_csv(BUFF_DIR / f"{buff_preset_name}.csv", index=False)
        buff_preset_read_name = st.selectbox(
            "バフプリセット名", [f.stem for f in BUFF_DIR.glob("*.csv")]
        )
        if st.button("バフ読み込み"):
            st.session_state.buff = pd.read_csv(
                BUFF_DIR / f"{buff_preset_read_name}.csv"
            )
            st.rerun()
    st.session_state.buff_list_df = buff_list_df


def debuff_df_input():
    with st.expander("デバフ入力", expanded=True):
        column_config = {
            "デバフ種": SelectboxColumn(
                options=list(map(lambda x: x.value, Debuff.__members__.values())),
                width=200,
                required=True,
            ),
            "デバフ量": NumberColumn(required=True),
            "備考": TextColumn(width=200),
        }
        if "debuff" not in st.session_state:
            data = {
                "デバフ種": [],
                "デバフ量": [],
                "備考": [],
            }
            debuff_list_df = pd.DataFrame(data).astype(
                {"デバフ種": "str", "デバフ量": "float", "備考": "str"}
            )
        else:
            debuff_list_df = st.session_state.debuff
        debuff_list_df = st.data_editor(
            debuff_list_df, column_config=column_config, num_rows="dynamic"
        )
        debuff_list_df = debuff_list_df[["デバフ種", "デバフ量", "備考"]].reset_index(
            drop=True
        )

    with st.expander("デバフプリセット保存・読み込み", expanded=False):
        debuff_preset_name = st.text_input("デバフプリセット名")
        if st.button("デバフ保存"):
            if (DEBUFF_DIR / f"{debuff_preset_name}.csv").exists():
                debuff_list_df.to_csv(
                    DEBUFF_DIR / f"{debuff_preset_name}.csv", index=False
                )
                st.warning("同名のデバフプリセットを上書きしました。")
            else:
                debuff_list_df.to_csv(
                    DEBUFF_DIR / f"{debuff_preset_name}.csv", index=False
                )
        debuff_preset_read_name = st.selectbox(
            "デバフプリセット名", [f.stem for f in DEBUFF_DIR.glob("*.csv")]
        )
        if st.button("デバフ読み込み"):
            st.session_state.debuff = pd.read_csv(
                DEBUFF_DIR / f"{debuff_preset_read_name}.csv"
            )
            st.rerun()
    st.session_state.debuff_list_df = debuff_list_df
