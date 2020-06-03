from apiclient import errors
import base64
import email

"""Get a list of Messages from the user's mailbox.
"""

def ListMessagesMatchingQuery(service, user_id, query=''):
	"""List all Messages of the user's mailbox matching the query.

	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		query: String used to filter messages returned.
		Eg.- 'from:user@some_domain.com' for Messages from a particular sender.

	Returns:
		List of Messages that match the criteria of the query. Note that the
		returned list contains Message IDs, you must use get with the
		appropriate ID to get the details of a Message.
	"""
	try:
		response = service.users().messages().list(userId=user_id, q=query).execute()
		messages = []
		if 'messages' in response:
			messages.extend(response['messages'])

		while 'nextPageToken' in response:
			page_token = response['nextPageToken']
			response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
			messages.extend(response['messages'])

		return messages
	except errors.HttpError as error:
		print('An error occurred: %s' % error)




"""Retrieve an attachment from a Message.
"""

def GetAttachments(service, user_id, msg_id, store_dir):
	"""Get and store attachment from Message with given id.

	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		msg_id: ID of Message containing attachment.
		store_dir: The directory used to store attachments.
	"""
	try:
		message = service.users().messages().get(userId=user_id, id=msg_id).execute()

		for part in message['payload']['parts']:
			if part['filename']:
				attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=part['body']['attachmentId']).execute()
				file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

				path = ''.join([store_dir, part['filename']])

				f = open(path, 'wb')
				f.write(file_data)
				f.close()

				return f"Downloaded {part['filename']} into {path}."

	except errors.HttpError as error:
		print('An error occurred: %s' % error)

def ModifyMessage(service, user_id, msg_id, msg_labels):
	"""Modify the Labels on the given Message.

	Args:
		service: Authorized Gmail API service instance.
		user_id: User's email address. The special value "me"
		can be used to indicate the authenticated user.
		msg_id: The id of the message required.
		msg_labels: The change in labels.

	Returns:
		Modified message, containing updated labelIds, id and threadId.
	"""
	try:
		message = service.users().messages().modify(userId=user_id, id=msg_id,body=msg_labels).execute()
																								

		label_ids = message['labelIds']

		# print('Message ID: %s - With Label IDs %s' % (msg_id, label_ids))
		return message
	except errors.HttpError as error:
		print('An error occurred: %s' % error)