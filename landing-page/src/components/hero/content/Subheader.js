import React from 'react'
import { css } from 'linaria' // eslint-disable-line

const subheader = css`
  font-size: 1rem;
  font-weight: 400;
  margin: 28px 0 32px 12px;
`

function Subheader(props) {
  return <h2 className={subheader}>ReactJS, GraphQL, and Django inside</h2>
}

export default Subheader
