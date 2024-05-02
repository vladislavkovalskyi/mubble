import dataclasses
import typing

from fntypes.option import Nothing

import mubble.types
from mubble.msgspec_utils import Option

from .base import ComposeError, DataNode, ScalarNode
from .message import MessageNode


@dataclasses.dataclass
class Attachment(DataNode):
    attachment_type: typing.Literal["audio", "document", "photo", "poll", "video"]
    _: dataclasses.KW_ONLY
    audio: Option[mubble.types.Audio] = dataclasses.field(default_factory=lambda: Nothing())
    document: Option[mubble.types.Document] = dataclasses.field(default_factory=lambda: Nothing())
    photo: Option[list[mubble.types.PhotoSize]] = dataclasses.field(default_factory=lambda: Nothing())
    poll: Option[mubble.types.Poll] = dataclasses.field(default_factory=lambda: Nothing())
    video: Option[mubble.types.Video] = dataclasses.field(default_factory=lambda: Nothing())

    @classmethod
    async def compose(cls, message: MessageNode) -> "Attachment":
        for attachment_type in ("audio", "document", "photo", "poll", "video"):
            if (attachment := getattr(message, attachment_type, None)) is not None:
                return cls(attachment_type, **{attachment_type: attachment})
        return cls.compose_error("No attachment found in message")


@dataclasses.dataclass
class Photo(DataNode):
    sizes: list[mubble.types.PhotoSize]

    @classmethod
    async def compose(cls, attachment: Attachment) -> typing.Self:
        return cls(attachment.photo.expect(ComposeError("Attachment is not an photo")))


class Video(ScalarNode, mubble.types.Video):
    @classmethod
    async def compose(cls, attachment: Attachment) -> mubble.types.Video:
        return attachment.video.expect(ComposeError("Attachment is not an video"))


class Audio(ScalarNode, mubble.types.Audio):
    @classmethod
    async def compose(cls, attachment: Attachment) -> mubble.types.Audio:
        return attachment.audio.expect(ComposeError("Attachment is not an audio"))


class Document(ScalarNode, mubble.types.Document):
    @classmethod
    async def compose(cls, attachment: Attachment) -> mubble.types.Document:
        return attachment.document.expect(ComposeError("Attachment is not an document"))


class Poll(ScalarNode, mubble.types.Poll):
    @classmethod
    async def compose(cls, attachment: Attachment) -> mubble.types.Poll:
        return attachment.poll.expect(ComposeError("Attachment is not an poll"))


__all__ = (
    "Attachment",
    "Audio",
    "Document",
    "Photo",
    "Poll",
    "Video",
)
