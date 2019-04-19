import React from 'react'
import PropTypes from 'prop-types'
import styled from 'styled-components'
import { Mutation } from 'react-apollo'
import MaterialIcon from '@material/react-material-icon';
// queries
import { ALL_NOTES, DELETE_NOTES } from "./../queries"

export const DeleteOptionStyledMaterialIcon = styled(MaterialIcon)`
  line-height: 48px;
`

function DeleteOption(props) {
  const handleDeletion = (cache, { data: { deleteNotes: { deletedNotes } } }) => {
    var cacheData = cache.readQuery({ query: ALL_NOTES })
    // remaping notes with correct cursors
    var deletedNotesIDs = []
    deletedNotes.forEach(note => {
      deletedNotesIDs.push(note.id)
    })
    // remember cursors and filter Nodes
    var allCursors = []
    var freshNodes = []
    cacheData.allNotes.edges.forEach(edge => {
      allCursors.push(edge.cursor)
      !deletedNotesIDs.includes(edge.node.id) && freshNodes.push(edge.node)
    })
    // prototype of new edges
    var newEdges = []
    freshNodes.forEach((node, index) => {
      newEdges.push({
        cursor: allCursors[index], 
        node: node,
        __typename: "NoteNodeEdge"
      })
    })
    // prototype of the end cursor
    const endCursor = allCursors[newEdges.length - 1]
    cacheData.allNotes.edges = newEdges // include new edges into the cache
    cacheData.allNotes.pageInfo.endCursor = endCursor // reset end cursor
    cache.writeQuery({ query: ALL_NOTES, data: cacheData })
  }

  return (
    <Mutation
      mutation={DELETE_NOTES}
      update={handleDeletion}
      variables={{ ids: [props.node.id] }}
    >
      {deleteNotes => (
        <DeleteOptionStyledMaterialIcon onClick={deleteNotes} className="item" icon='delete' />
      )}
    </Mutation>
  )
}

DeleteOption.propTypes = {
  node: PropTypes.object,
}

export default DeleteOption