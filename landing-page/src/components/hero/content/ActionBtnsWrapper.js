import React from 'react'
import { css } from 'linaria' // eslint-disable-line

const wrapper = css`
  display: flex;
  align-items: center;
  margin: 0 0 0 -12px;
`

function ActionBtnsWrapper(props) {
  return <div className={wrapper}>{props.children}</div>
}

export default ActionBtnsWrapper
